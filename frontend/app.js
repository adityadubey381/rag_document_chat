// DocuMind AI - Frontend Controller

document.addEventListener('DOMContentLoaded', () => {
    // State management
    let documents = [];
    let topK = 4;
    let isUploading = false;
    let isWaitingForAI = false;

    // DOM Elements Cache
    const sidebar = document.getElementById('sidebar');
    const openSidebarBtn = document.getElementById('openSidebarBtn');
    const closeSidebarBtn = document.getElementById('closeSidebarBtn');
    const settingsToggleBtn = document.getElementById('settingsToggleBtn');
    const settingsDropdown = document.getElementById('settingsDropdown');
    const clearChatBtn = document.getElementById('clearChatBtn');
    
    const uploadZone = document.getElementById('uploadZone');
    const fileInput = document.getElementById('fileInput');
    const selectFilesBtn = document.getElementById('selectFilesBtn');
    const uploadProgressContainer = document.getElementById('uploadProgressContainer');
    const uploadingFileName = document.getElementById('uploadingFileName');
    const progressBarFill = document.getElementById('progressBarFill');
    const uploadProgressPercent = document.getElementById('uploadProgressPercent');
    
    const documentsList = document.getElementById('documentsList');
    const docCount = document.getElementById('docCount');
    const chatHistory = document.getElementById('chatHistory');
    const welcomeContainer = document.getElementById('welcomeContainer');
    const chatForm = document.getElementById('chatForm');
    const messageInput = document.getElementById('messageInput');
    const sendBtn = document.getElementById('sendBtn');
    const topKSlider = document.getElementById('topKSlider');
    const topKVal = document.getElementById('topKVal');

    // Initialize Markdown parser configurations
    marked.setOptions({
        breaks: true,
        sanitize: false, // Allow HTML tags if any (custom rendering)
        highlight: function(code, lang) {
            if (Prism.languages[lang]) {
                return Prism.highlight(code, Prism.languages[lang], lang);
            }
            return code;
        }
    });

    // ----------------------------------------------------
    // API Communication Methods
    // ----------------------------------------------------

    // Fetch list of all indexed documents
    async function fetchDocuments() {
        try {
            const response = await fetch('/api/v1/documents');
            if (!response.ok) throw new Error('Failed to load documents.');
            
            documents = await response.json();
            updateDocumentsUI();
        } catch (error) {
            console.error('Error fetching documents:', error);
            showNotification('Error loading documents list', 'error');
        }
    }

    // Upload files sequentially
    async function uploadFiles(files) {
        if (files.length === 0) return;
        isUploading = true;
        setUploadUIActive(true);

        for (let i = 0; i < files.length; i++) {
            const file = files[i];
            uploadingFileName.textContent = `Uploading: ${file.name}`;
            
            const formData = new FormData();
            formData.append('file', file);

            try {
                // Fetch wrapper with fake progress increments (since native fetch doesn't support upload progress cleanly)
                const uploadPromise = fetch('/api/v1/upload', {
                    method: 'POST',
                    body: formData
                });

                // Simulate progress updates
                let progress = 0;
                const interval = setInterval(() => {
                    if (progress < 90) {
                        progress += 10;
                        updateProgress(progress);
                    }
                }, 100);

                const response = await uploadPromise;
                clearInterval(interval);
                updateProgress(100);

                if (!response.ok) {
                    const errDetail = await response.json();
                    throw new Error(errDetail.detail || `Ingestion failed for ${file.name}`);
                }

                showNotification(`Successfully indexed: ${file.name}`, 'success');
            } catch (error) {
                console.error(`Upload error for ${file.name}:`, error);
                showNotification(error.message, 'error');
            }
            
            // Rest progress slightly before next file
            await new Promise(r => setTimeout(r, 400));
            updateProgress(0);
        }

        isUploading = false;
        setUploadUIActive(false);
        await fetchDocuments();
    }

    // Delete document by ID
    async function deleteDocument(documentId, filename) {
        if (!confirm(`Are you sure you want to delete and un-index "${filename}"? This action cannot be undone.`)) return;

        try {
            const response = await fetch(`/api/v1/documents/${documentId}`, {
                method: 'DELETE'
            });

            if (!response.ok) throw new Error('Deletion request failed.');

            showNotification(`Deleted: ${filename}`, 'success');
            await fetchDocuments();
        } catch (error) {
            console.error('Error deleting document:', error);
            showNotification(`Failed to delete document: ${error.message}`, 'error');
        }
    }

    // Submit natural language query to the LLM (RAG pipeline)
    async function submitChatQuery(message) {
        if (!message.trim() || isWaitingForAI) return;

        // Reset text area height
        messageInput.value = '';
        messageInput.style.height = 'auto';
        sendBtn.disabled = true;

        // 1. Add User Message Bubble
        appendMessageBubble(message, 'user');
        welcomeContainer.style.display = 'none';
        
        // 2. Add Typing Indicator Bubble
        const typingBubble = appendTypingIndicator();
        scrollChatToBottom();

        isWaitingForAI = true;
        toggleInputState(false);

        try {
            const response = await fetch('/api/v1/chat/query', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    message: message,
                    top_k: topK
                })
            });

            // Remove typing bubble
            typingBubble.remove();

            if (!response.ok) {
                const errDetail = await response.json();
                throw new Error(errDetail.detail || 'RAG AI processing failed.');
            }

            const data = await response.json(); // returns { answer: str, sources: [{filename, file_type, chunk_index, ...}] }
            
            // 3. Append Assistant Answer Bubble
            appendMessageBubble(data.answer, 'assistant', data.sources);
        } catch (error) {
            console.error('Chat error:', error);
            // Append error message bubble
            appendMessageBubble(`⚠️ **Error processing request**: ${error.message}. Please verify the backend service is running and configured correctly.`, 'assistant');
        } finally {
            isWaitingForAI = false;
            toggleInputState(true);
            scrollChatToBottom();
            messageInput.focus();
        }
    }

    // ----------------------------------------------------
    // UI Rendering & Manipulation
    // ----------------------------------------------------

    // Update the files sidebar UI list
    function updateDocumentsUI() {
        docCount.textContent = documents.length;

        if (documents.length === 0) {
            documentsList.innerHTML = `
                <div class="empty-docs-state">
                    <i class="fa-regular fa-folder-open"></i>
                    <p>No documents uploaded yet</p>
                </div>
            `;
            toggleInputState(false);
            return;
        }

        toggleInputState(true);
        documentsList.innerHTML = '';

        documents.forEach(doc => {
            const item = document.createElement('div');
            item.className = 'document-item';
            
            let iconClass = 'fa-file-lines doc-icon txt';
            let fileExtClass = 'txt';
            const ext = doc.file_type.toLowerCase();
            
            if (ext === '.pdf') {
                iconClass = 'fa-file-pdf doc-icon pdf';
                fileExtClass = 'pdf';
            } else if (ext === '.docx') {
                iconClass = 'fa-file-word doc-icon docx';
                fileExtClass = 'docx';
            }

            item.innerHTML = `
                <div class="doc-info">
                    <div class="doc-icon ${fileExtClass}">
                        <i class="fa-solid ${iconClass}"></i>
                    </div>
                    <div class="doc-details">
                        <div class="doc-name" title="${doc.filename}">${doc.filename}</div>
                        <div class="doc-size">ID: ${doc.document_id.substring(0, 8)}...</div>
                    </div>
                </div>
                <button class="delete-doc-btn" data-id="${doc.document_id}" data-name="${doc.filename}" title="Un-index File">
                    <i class="fa-solid fa-trash-can"></i>
                </button>
            `;

            // Bind delete event
            item.querySelector('.delete-doc-btn').addEventListener('click', (e) => {
                const btn = e.currentTarget;
                deleteDocument(btn.dataset.id, btn.dataset.name);
            });

            documentsList.appendChild(item);
        });
    }

    // Enable/Disable chat input fields
    function toggleInputState(enable) {
        const canType = enable && documents.length > 0 && !isWaitingForAI;
        messageInput.disabled = !canType;
        
        if (canType) {
            messageInput.placeholder = "Ask a question about your documents...";
            sendBtn.disabled = !messageInput.value.trim();
        } else {
            if (documents.length === 0) {
                messageInput.placeholder = "⚠️ Ingest a document first to start chatting...";
            } else if (isWaitingForAI) {
                messageInput.placeholder = "AI is thinking...";
            }
            sendBtn.disabled = true;
        }
    }

    // Append a message bubble to the chat panel history
    function appendMessageBubble(content, role, sources = []) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `chat-message ${role}`;

        const avatar = document.createElement('div');
        avatar.className = 'msg-avatar';
        avatar.innerHTML = role === 'user' ? '<i class="fa-solid fa-user"></i>' : '<i class="fa-solid fa-robot"></i>';

        const bodyWrapper = document.createElement('div');
        bodyWrapper.className = 'msg-body-wrapper';

        const bubble = document.createElement('div');
        bubble.className = 'msg-bubble';
        
        if (role === 'user') {
            bubble.textContent = content;
        } else {
            // Render Markdown parsed HTML for assistant response
            bubble.innerHTML = marked.parse(content);
        }

        bodyWrapper.appendChild(bubble);

        // Add Citations Accordion if sources are referenced in RAG
        if (role === 'assistant' && sources && sources.length > 0) {
            const citationsContainer = document.createElement('div');
            citationsContainer.className = 'citations-container';

            const toggleBtn = document.createElement('button');
            toggleBtn.className = 'citations-toggle';
            toggleBtn.innerHTML = `<i class="fa-solid fa-chevron-right"></i> Refenced Contexts (${sources.length} matching segments)`;
            
            const panel = document.createElement('div');
            panel.className = 'citations-panel';

            // Populate source snippets
            sources.forEach((src, idx) => {
                const item = document.createElement('div');
                item.className = 'citation-item';
                
                const fileIcon = src.file_type === '.pdf' ? 'fa-file-pdf text-danger' : 
                                 src.file_type === '.docx' ? 'fa-file-word text-primary' : 'fa-file-lines text-success';
                
                item.innerHTML = `
                    <div class="citation-header">
                        <i class="fa-solid ${fileIcon}"></i>
                        <span>${src.filename || 'Unknown Document'}</span>
                        <span class="doc-count">Section Index: ${src.chunk_index !== undefined ? src.chunk_index : 'N/A'}</span>
                    </div>
                `;
                panel.appendChild(item);
            });

            // Toggle expand collapse action
            toggleBtn.addEventListener('click', () => {
                const isExpanded = toggleBtn.classList.toggle('expanded');
                panel.style.display = isExpanded ? 'flex' : 'none';
                if (isExpanded) {
                    toggleBtn.innerHTML = `<i class="fa-solid fa-chevron-down"></i> Referenced Contexts (${sources.length} matching segments)`;
                } else {
                    toggleBtn.innerHTML = `<i class="fa-solid fa-chevron-right"></i> Referenced Contexts (${sources.length} matching segments)`;
                }
                scrollChatToBottom();
            });

            citationsContainer.appendChild(toggleBtn);
            citationsContainer.appendChild(panel);
            bodyWrapper.appendChild(citationsContainer);
        }

        messageDiv.appendChild(avatar);
        messageDiv.appendChild(bodyWrapper);
        chatHistory.appendChild(messageDiv);

        // Apply syntax highlighting inside code elements
        if (role === 'assistant') {
            Prism.highlightAllUnder(bubble);
        }
    }

    // Append AI Typing indicator loader
    function appendTypingIndicator() {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'chat-message assistant';

        const avatar = document.createElement('div');
        avatar.className = 'msg-avatar';
        avatar.innerHTML = '<i class="fa-solid fa-robot"></i>';

        const bodyWrapper = document.createElement('div');
        bodyWrapper.className = 'msg-body-wrapper';

        const bubble = document.createElement('div');
        bubble.className = 'typing-indicator';
        bubble.innerHTML = `
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        `;

        bodyWrapper.appendChild(bubble);
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(bodyWrapper);
        chatHistory.appendChild(messageDiv);

        return messageDiv;
    }

    // Update progress bar percentage values
    function updateProgress(percent) {
        progressBarFill.style.width = `${percent}%`;
        uploadProgressPercent.textContent = `${percent}%`;
    }

    function setUploadUIActive(active) {
        if (active) {
            uploadProgressContainer.style.display = 'block';
            selectFilesBtn.disabled = true;
            uploadZone.classList.add('dragover');
        } else {
            uploadProgressContainer.style.display = 'none';
            selectFilesBtn.disabled = false;
            uploadZone.classList.remove('dragover');
            updateProgress(0);
        }
    }

    // Helper notifications
    function showNotification(message, type = 'success') {
        const notif = document.createElement('div');
        notif.style.position = 'fixed';
        notif.style.bottom = '20px';
        notif.style.right = '20px';
        notif.style.padding = '12px 24px';
        notif.style.borderRadius = '8px';
        notif.style.color = '#fff';
        notif.style.fontSize = '0.85rem';
        notif.style.fontWeight = '600';
        notif.style.zIndex = '9999';
        notif.style.boxShadow = '0 4px 12px rgba(0,0,0,0.5)';
        notif.style.animation = 'fadeInUp 0.25s ease forwards';
        
        if (type === 'success') {
            notif.style.backgroundColor = 'var(--success)';
            notif.innerHTML = `<i class="fa-solid fa-circle-check"></i> ${message}`;
        } else {
            notif.style.backgroundColor = 'var(--error)';
            notif.innerHTML = `<i class="fa-solid fa-circle-exclamation"></i> ${message}`;
        }

        document.body.appendChild(notif);
        setTimeout(() => {
            notif.style.animation = 'fadeOutDown 0.25s ease forwards';
            setTimeout(() => notif.remove(), 250);
        }, 3000);
    }

    // Autoscroll chat history container to newest bubble
    function scrollChatToBottom() {
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }

    // ----------------------------------------------------
    // User Action Event Listeners
    // ----------------------------------------------------

    // Responsive Mobile Navigation Sidebars
    openSidebarBtn.addEventListener('click', () => sidebar.classList.add('open'));
    closeSidebarBtn.addEventListener('click', () => sidebar.classList.remove('open'));

    // Parameter Range sliders
    topKSlider.addEventListener('input', (e) => {
        topK = parseInt(e.target.value);
        topKVal.textContent = topK;
    });

    // Toggle Settings panel
    settingsToggleBtn.addEventListener('click', () => {
        const isClosed = settingsDropdown.style.display === 'none' || !settingsDropdown.style.display;
        settingsDropdown.style.display = isClosed ? 'block' : 'none';
        settingsToggleBtn.classList.toggle('active', isClosed);
    });

    // Clear Chats
    clearChatBtn.addEventListener('click', () => {
        if (chatHistory.children.length <= 1) return; // Only welcome view or empty
        if (!confirm('Clear all conversation messages?')) return;
        
        // Remove all bubbles except welcome
        const bubbles = chatHistory.querySelectorAll('.chat-message');
        bubbles.forEach(b => b.remove());
        welcomeContainer.style.display = 'flex';
    });

    // File selection clicks
    selectFilesBtn.addEventListener('click', () => {
        if (!isUploading) fileInput.click();
    });
    
    fileInput.addEventListener('change', (e) => {
        uploadFiles(e.target.files);
    });

    // Drag-and-Drop Ingestions
    uploadZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        if (!isUploading) uploadZone.classList.add('dragover');
    });

    uploadZone.addEventListener('dragleave', () => {
        uploadZone.classList.remove('dragover');
    });

    uploadZone.addEventListener('drop', (e) => {
        e.preventDefault();
        if (isUploading) return;
        uploadZone.classList.remove('dragover');
        uploadFiles(e.dataTransfer.files);
    });

    // Send Form submissions
    chatForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const msg = messageInput.value.trim();
        if (msg) submitChatQuery(msg);
    });

    // Manage Enter/Submit vs Shift+Enter linebreaks on textareas
    messageInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            chatForm.dispatchEvent(new Event('submit'));
        }
    });

    // Auto-growing input box
    messageInput.addEventListener('input', () => {
        messageInput.style.height = 'auto';
        messageInput.style.height = `${messageInput.scrollHeight}px`;
        sendBtn.disabled = !messageInput.value.trim() || isWaitingForAI;
    });

    // ----------------------------------------------------
    // Bootstrap initialization
    // ----------------------------------------------------
    fetchDocuments();
});

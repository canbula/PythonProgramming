document.addEventListener('DOMContentLoaded', function() {
    const workspaceHeader = document.querySelector('.workspace-header');
    const dropdownMenu = document.querySelector('.workspace-header .dropdown-menu');
    const addWorkspaceBtn = document.getElementById('add-workspace-btn');
    const privateToggle = document.getElementById('private-toggle');
    const privatePages = document.getElementById('private-pages');
    const savePageBtn = document.getElementById('save-page-btn');

    let activePageId = null;

    workspaceHeader.addEventListener('mouseenter', function() {
        dropdownMenu.style.display = 'block';
    });

    workspaceHeader.addEventListener('mouseleave', function() {
        setTimeout(function() {
            if (!workspaceHeader.matches(':hover') && !dropdownMenu.matches(':hover')) {
                dropdownMenu.style.display = 'none';
            }
        }, 300);
    });

    dropdownMenu.addEventListener('mouseenter', function() {
        dropdownMenu.style.display = 'block';
    });

    dropdownMenu.addEventListener('mouseleave', function() {
        dropdownMenu.style.display = 'none';
    });

    addWorkspaceBtn.addEventListener('click', function(event) {
        event.preventDefault();
        fetch('/notes/create_workspace/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.id) {
                const existingWorkspace = document.querySelector(`.dropdown-item[href="?workspace_id=${data.id}"]`);
                if (!existingWorkspace) {
                    const newWorkspace = document.createElement('a');
                    newWorkspace.classList.add('dropdown-item', 'd-flex', 'align-items-center');
                    newWorkspace.href = `?workspace_id=${data.id}`;
                    newWorkspace.innerHTML = `
                        <div class="workspace-info d-flex align-items-center">
                            <i class="fa-solid fa-w workspace-icon-small"></i>
                            <div>
                                <div>${data.name}</div>
                                <small class="text-muted">${data.members_count} member${data.members_count !== 1 ? 's' : ''}</small>
                            </div>
                        </div>
                    `;
                    dropdownMenu.insertBefore(newWorkspace, dropdownMenu.children[1]);
                }
            } else {
                alert('Error creating workspace');
            }
        });
    });

    privateToggle.addEventListener('click', function() {
        if (privatePages.style.display === 'none') {
            privatePages.style.display = 'block';
        } else {
            privatePages.style.display = 'none';
        }
    });

    document.querySelectorAll('.ellipsis-icon').forEach(icon => {
        icon.addEventListener('click', function(event) {
            event.stopPropagation();
            const pageId = icon.getAttribute('data-page-id');
            const dropdownMenu = document.querySelector(`.page-dropdown-menu[data-page-id="${pageId}"]`);
            if (dropdownMenu.style.display === 'block') {
                dropdownMenu.style.display = 'none';
            } else {
                document.querySelectorAll('.page-dropdown-menu').forEach(menu => {
                    menu.style.display = 'none';
                });
                dropdownMenu.style.display = 'block';
            }
        });
    });

    document.querySelectorAll('.dropdown-item[data-action]').forEach(item => {
        item.addEventListener('click', function(event) {
            event.preventDefault();
            const action = item.getAttribute('data-action');
            const pageId = item.getAttribute('data-page-id');
            if (action === 'delete') {
                handleDelete(pageId);
            } else if (action === 'copy-link') {
                handleCopyLink(pageId);
            } else if (action === 'duplicate') {
                handleDuplicate(pageId);
            }
        });
    });

    function handleDelete(pageId) {
        if (confirm('Are you sure you want to delete this page?')) {
            fetch(`/notes/delete_page/${pageId}/`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(response => {
                if (response.ok) {
                    location.reload();
                } else {
                    alert('Error deleting page');
                }
            });
        }
    }

    function handleCopyLink(pageId) {
        const link = `${window.location.origin}/notes/?page_id=${pageId}`;
        navigator.clipboard.writeText(link).then(() => {
            alert('Link copied to clipboard');
        });
    }

    function handleDuplicate(pageId) {
        fetch(`/notes/duplicate_page/${pageId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => {
            if (response.ok) {
                location.reload();
            } else {
                alert('Error duplicating page');
            }
        });
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function loadPage(pageId) {
        fetch(`/notes/get_page_details/${pageId}/`)
            .then(response => response.json())
            .then(data => {
                console.log('Page Data:', data); // Log the data to ensure it's being fetched correctly
                const pageTitleInput = document.getElementById('page-title-input');
                const pageContent = document.getElementById('page-content');

                if (pageTitleInput && pageContent) {
                    pageTitleInput.value = data.title;
                    pageContent.value = data.content; // Set the page content

                    document.querySelectorAll('.nav-link').forEach(link => link.classList.remove('active'));
                    document.querySelector(`[data-page-id="${pageId}"]`).closest('.nav-link').classList.add('active');

                    activePageId = pageId; // Update the active page ID
                } else {
                    console.error('Page title input or page content element not found.');
                }
            })
            .catch(error => {
                console.error('Error loading page:', error);
            });
    }

    function getCurrentWorkspaceId() {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get('workspace_id');
    }

    const pageTitleInput = document.getElementById('page-title-input');
    const pageContentInput = document.getElementById('page-content');

    function updatePageTitleAndContent() {
        if (!activePageId) return;
        const newTitle = pageTitleInput.value;
        const newContent = pageContentInput.value;
        fetch(`/notes/update_page_title/${activePageId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: `title=${encodeURIComponent(newTitle)}&content=${encodeURIComponent(newContent)}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById(`page-title-${activePageId}`).innerText = newTitle;
                alert('Page updated successfully');
            } else {
                alert(data.error);
            }
        });
    }

    if (savePageBtn) {
        savePageBtn.addEventListener('click', function() {
            updatePageTitleAndContent();
        });
    }

    window.loadPage = loadPage;
});

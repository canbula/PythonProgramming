document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-input');
    searchInput.addEventListener('input', function() {
        const query = searchInput.value;
        const form = document.getElementById('search-form');
        fetch(`${form.action}?q=${query}`, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.text())
        .then(data => {
            document.getElementById('search-results').innerHTML = data;
        })
        .catch(error => console.error('Error:', error));
    });
});

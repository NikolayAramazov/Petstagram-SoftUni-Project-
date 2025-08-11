const form = document.getElementById('searchForm');

form.addEventListener('submit', (e) => {
  e.preventDefault();

const formData = new FormData(form);
const params = new URLSearchParams(formData).toString();

if(form){
  fetch(`${form.action}?${params}`, {
      method: 'get',
      headers: {
          'X-Requested-With': 'XMLHttpRequest'
      },
    })
    .then(response => response.text())
    .then(html => {
      document.getElementById('profilesContainer').innerHTML = html;
    })
    .catch(error => {
        console.error('Error:', error)
    })
  }
})
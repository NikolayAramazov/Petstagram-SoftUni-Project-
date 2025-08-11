document.addEventListener('DOMContentLoaded', () => {
  const forms = document.querySelectorAll('.comment-form');

  forms.forEach(form => {
    form.addEventListener('submit', (e) => {
      e.preventDefault();

      const formData = new FormData(form);

      fetch(form.action, {
        method: 'post',
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
        },
        body: formData
      })
      .then(response => response.text())
      .then(html => {
        const container = form.closest('.bottom').querySelector('.comments');
        container.insertAdjacentHTML('afterbegin', html);
        form.reset();
      })
      .catch(error => {
        console.error('Error:', error);
      });
    });
  });
});

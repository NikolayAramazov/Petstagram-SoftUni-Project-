document.addEventListener('DOMContentLoaded', () => {
  const likeForms = document.querySelectorAll('.like_form');

  likeForms.forEach(form => {
    form.addEventListener('submit', (e) => {
      e.preventDefault();

      const hearthIcon = form.querySelector('.fa-heart');
      const likesCountElem = form.closest('.bottom').querySelector('.likes');

      const formData = new FormData(form);

      fetch(form.action, {
        method: 'POST',
        headers: {
          'X-Requested-With': 'XMLHttpRequest'
        },
        body: formData,
      })
      .then(response => {
        if (!response.ok) throw new Error('Network error');
        return response.json();
      })
      .then(data => {
        if (data.liked) {
          hearthIcon.classList.remove('fa-regular');
          hearthIcon.classList.add('fa-solid');
          hearthIcon.style.color = '#ed4040';
        } else {
          hearthIcon.classList.remove('fa-solid');
          hearthIcon.classList.add('fa-regular');
          hearthIcon.style.color = '';
        }
        if (likesCountElem) {
          likesCountElem.textContent = `${data.likes_count} like${data.likes_count !== 1 ? 's' : ''}`;
        }
      })
      .catch(error => {
        console.error('Error liking photo:', error);
      });
    });
  });
});
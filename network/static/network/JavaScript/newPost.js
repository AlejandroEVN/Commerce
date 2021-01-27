document.addEventListener("DOMContentLoaded", () => {
    const btnNewPost = document.querySelector('.btn-new-post');
    const newPost = document.querySelector('.new-post');

    btnNewPost.addEventListener('click', () => {
        newPost.classList.toggle('show');
    })
})
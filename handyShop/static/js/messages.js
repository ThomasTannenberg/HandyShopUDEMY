
window.onload = function () {
    const popup = document.querySelector('.messages-popup');
    popup.style.visibility = 'visible';
    setTimeout(() => {
        popup.style.visibility = 'hidden';
    }, 900);
};

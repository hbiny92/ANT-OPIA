const welcomeSection = document.querySelector('.welcome-section')
const enterButton = document.querySelector('.enter-button')
setTimeout(() => {
    welcomeSection.classList.remove('content-hidden')
}, 800)
enterButton.addEventListener('click', (e) => {
    e.preventDefault()
    welcomeSection.classList.add('content-hidden')
    setTimeout(() => {
        welcomeSection.style.opacity = 0;
    }, 800)
})
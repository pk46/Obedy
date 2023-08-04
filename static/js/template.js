function scrollToElement(element) {
  let targetElement = document.getElementById(element.dataset.restaurant);

  let navbarHeight = document.getElementById('menu').offsetHeight;
  let targetPosition = targetElement.offsetTop - navbarHeight;

  window.scrollTo({
    top: targetPosition,
    behavior: 'smooth'
  });
}

// delay function
function delay(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

document.addEventListener('DOMContentLoaded', function () {
  const slideList = document.querySelectorAll('.app-slide-content');
  const appButtonlist = document.querySelectorAll('.app-button');
  const prevButton = document.querySelector('.app-slide-nav-before');
  const nextButton = document.querySelector('.app-slide-nav-after');

	// init slider
	let activeKey = 0;
	slideList[activeKey].classList.add('active');

	// change slide
	async function onSlideChange(key) {
    key = (key % slideList.length + slideList.length) % slideList.length;
	  if (key === activeKey) return;
	  slideList[activeKey].classList.add('leave');
	  await delay(400);
	  slideList[activeKey].classList.remove('leave', 'active');
	  activeKey = key;
	  slideList[key].classList.add('active');
	}
  
  // add button function
	appButtonlist.forEach((button, key) => {
	  button.addEventListener('click', () => onSlideChange(key))
  })
  
  // add arrow function
  prevButton.addEventListener('click', () => onSlideChange(activeKey - 1));
  nextButton.addEventListener('click', () => onSlideChange(activeKey + 1));
});

document.addEventListener('DOMContentLoaded', function () {
  const debounce = (fn) => {
    // This holds the requestAnimationFrame reference, so we can cancel it if we wish
    let frame;
  
    return (...params) => {
      // If the frame variable has been defined, clear it now, and queue for next frame
      if (frame) {
        cancelAnimationFrame(frame);
      }
  
      // Queue our function call for the next frame
      frame = requestAnimationFrame(() => {
        fn(...params);
      });
    };
  };
    
  // Reads out the scroll position and stores it in the data attribute
  // so we can use it in our stylesheets
  const storeScroll = () => {
    document.documentElement.dataset.scroll = window.scrollY;
  };
  
  // Listen for new scroll events, here we debounce our `storeScroll` function
  document.addEventListener("scroll", debounce(storeScroll), { passive: true });
  
  // Update scroll position for first time
  storeScroll();
});
function getThumbBounds(index) {
  // Get the proper grid item
  let tabindex = index+1;
  let selector = '.grid-item[tabindex="'+tabindex+'"]'
  let grid_item = $(selector);

  // Then find the contained image
  let thumbnail = $(grid_item).find('img')[0];

  // get position of element relative to viewport
  let pageYScroll = window.pageYOffset || document.documentElement.scrollTop;
  let rect = thumbnail.getBoundingClientRect();
  return {
    x: rect.left,
    y: rect.top + pageYScroll,
    w: rect.width
  };
}

function buildPhotoSwipeItems(photos_info_data) {
  let ps_items = [];
  photos_info_data.forEach(photo => {
    ps_items.push({
      src: 'assets/img/photos/' + photo.large,
      msrc: 'assets/img/photos/' + photo.thumb,
      w: photo.large_width,
      h: photo.large_height,
      pid: photo.title,
      title: photo.title,
      author: "Nick Crews"
    });
  });
  return ps_items;
}

function openPhotoSwipe(items, index = 0) {
  var pswpElement = $('.pswp')[0];

  var options = {
    index: index,
    bgOpacity: .8,
    // Use the title of the photo (instead of the index) as the URL photo ID
    galleryPIDs: true,
    // Time to hide the swipe controls in msec
    timeToIdle: 2000,
    // Disable some of the buttons in the UI
    counterEl: false,
    shareEl: false,
    getThumbBoundsFn: getThumbBounds,
    // fractional amount of spacing between images when swiping
    spacing: .05
  };

  var gallery = new PhotoSwipe(pswpElement, PhotoSwipeUI_Default, items, options);
  gallery.init();
}

function photo_clicked(event) {
  // The photo is actually a link, but we don't want to open the link.
  // If someone really wants to, or doesn't have javascript, they
  // can use the link to view the phot full size.
  event.preventDefault();
  // Which photo-grid-item this is, zero indexed.
  const ps_items = event.data;
  const index = parseInt($(this).attr("tabindex")) - 1;
  openPhotoSwipe(ps_items, index);
}

function initPhotoSwipe() {
  // Get the json attached to each DOM element in the "data-photos" attribute.
  let photos_info = $('.grid-item').map(function() {
    return $(this).data("photos");
  }).get();
  // Convert this into a list of item data for photoswipe.
  const ps_items = buildPhotoSwipeItems(photos_info);
  // Register callback.
  $('.grid-item').click(ps_items, photo_clicked);
}

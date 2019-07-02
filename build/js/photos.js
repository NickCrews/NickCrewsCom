// @photo: object with src, title, description fields
function addPhotoToDOM(photo) {
  $('.photo-grid').append(
    $('<div>', {
      class: 'photo-grid-item'
    }).prepend(
      $('<a>', {
        href: 'resources/images/photos/' + photo.full,
      }).prepend(
        $('<img>', {
          id: photo.title,
          src: 'resources/images/photos/' + photo.thumb,
          alt: photo.thumb,
        })
      )
    )
  )
}

function getThumbBounds(index) {
  // get the proper grid item, then find the contained image.
  var grid_item = $('.photo-grid-item')[index];
  var thumbnail = $(grid_item).find('a').find('img')[0];

  var pageYScroll = window.pageYOffset || document.documentElement.scrollTop;
  // optionally get horizontal scroll

  // get position of element relative to viewport
  var rect = thumbnail.getBoundingClientRect();
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
      src: 'resources/images/photos/' + photo.full,
      msrc: 'resources/images/photos/' + photo.thumb,
      w: photo.large_width,
      h: photo.large_height,
      pid: photo.title,
      title: photo.title,
      author: "Nick Crews"
    });
  });
  photo_swipe_items = ps_items;
  return ps_items;
}

function openPhotoSwipe(items, index = 0) {
  var pswpElement = $('.pswp')[0];

  var options = {
    index: index,
    bgOpacity: .8,
    // Use the title of the photo (instead of the index) as the URL photo ID
    galleryPIDs: true,
    timeToIdle: 2000,
    shareEl: false,
    getThumbBoundsFn: getThumbBounds,
    spacing: .05
  };

  var gallery = new PhotoSwipe(pswpElement, PhotoSwipeUI_Default, items, options);
  gallery.init();
  console.log(gallery.getZoomLevel());
}

function photo_clicked(event) {
  // The photo is actually a link, but we don't want to open the link.
  // If someone really wants to, or doesn't have javascript, they
  // can use the link to view the phot full size.
  event.preventDefault();
  // which photo-grid-item this is, zero indexed
  const index = $(this).index();
  openPhotoSwipe(buildPhotoSwipeItems(event.data), index);
}

function loadPhotos(photoJsonPath) {
  // $grid = $('.photo-grid').masonry({
  //   // options
  //   itemSelector: ".photo-grid-item",
  //   columnWidth: ".photo-grid-sizer",
  //   percentPosition: true
  // });

  let photo_data_loading = fetch(photoJsonPath).then(response => response.json());

  photo_data_loading.then(function(photos_data) {
    photos_data.forEach(photo => {
      addPhotoToDOM(photo);
    });
    $('.photo-grid-item').click(photos_data, photo_clicked);
    console.log("reloadGrid");
    reloadGrid();
  }).catch(error => console.log(error));
}

function reloadGrid() {
  // $grid.masonry('layout');

  $('.photo-grid').masonry({
    // options
    itemSelector: '.photo-grid-item',
    percentPosition: false
  });
}
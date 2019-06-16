// @photo: object with src, title, description fields
function addPhoto(photo) {
  $('.photo-grid').append(
    $('<div>', {
      class: 'photo-grid-item'
    }).prepend(
      $('<a>', {
        href: 'resources/images/photos/' + photo.src,
      }).prepend(
        $('<img>', {
          id: photo.src,
          src: 'resources/images/photos/' + photo.src,
          alt: photo.src,
        })
      )
    )
  )
}

// var $grid;

function loadPhotos(photoJsonPath) {
  // $grid = $( '.photo-grid' ).masonry( {
  //   // options
  //   itemSelector: '.photo-grid-item',
  //   columnWidth: '.photo-grid-sizer',
  //   percentPosition: true
  // } );

  let photo_data_loading = fetch(photoJsonPath).then(response => response.json());

  photo_data_loading.then(function(photo_data) {
    photo_data.forEach(photo => {
      addPhoto(photo);
    });
  }).catch(error => console.log(error));


}

function reloadGrid() {
  console.log('called');
  // $grid.masonry('layout');

  $('.photo-grid').masonry({
    // options
    itemSelector: '.photo-grid-item',
    columnWidth: '.photo-grid-item',
    percentPosition: false
  });
}
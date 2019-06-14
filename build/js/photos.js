// @photo: object with src, title, description fields
function addPhoto(photo) {
  $('.home').prepend($('<img>', {
    id: photo.src,
    src: 'resources/images/photos/' + photo.src,
    alt: photo.src,
  }));
}

function loadPhotos(photoJsonPath) {
  let photo_data_loading = fetch(photoJsonPath).
    then(response => response.json());

  photo_data_loading.then(function(photo_data) {
    photo_data.forEach(photo => {
      addPhoto(photo);
    });
  }).catch(error => console.log(error));
}

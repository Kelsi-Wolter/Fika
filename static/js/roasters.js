"use strict";



// Listen for click on "Add to favorites list" button on roaster details page --> creates new entry in list in DB for user
$('.add-fav').on('click', (evt) =>{
    evt.preventDefault();
    const roaster = $(evt.target);
    const roaster_id = {roaster: roaster.attr('id')};
    // console.log(roaster_id);
    $.get('/add_to_fav_list', roaster_id, (res) => {
        alert(res);
    });
    
})

// Same function as above but for roasters list
$('.add-roasters').on('click', (evt) =>{
    evt.preventDefault();
    const roaster = $(evt.target);
    const roaster_id = {roaster: roaster.attr('id')};
    // console.log(roaster_id);
    $.get('/add_to_roaster_list', roaster_id, (res) => {
        alert(res);
    });
    
})


// Shows editting buttons for favorites list entries when "edit list" button is clicked
$('.edit-fav').on('click', (evt) => {
    evt.preventDefault();
    
    const editBtn = evt.target;

    if (editBtn.innerHTML === 'Edit List') {
        editBtn.innerHTML = 'Done';
        $('.edit-fav-buttons').show();
      }
      else {
        editBtn.innerHTML = 'Edit List';
        $('.edit-fav-buttons').hide();
      };
    
});

// Same function as above but for roasters list entries
$('.edit-roasters').on('click', (evt) => {
    evt.preventDefault();

    const editBtn = evt.target;
    if(editBtn.innerHTML === 'Edit List') {
        editBtn.innerHTML = 'Done';
    $('.edit-roaster-buttons').show();
    }
    else {
        editBtn.innerHTML = 'Edit List';
        $('.edit-roaster-buttons').hide();
      };
    
});


// Moves entry to other list when move button is clicked
$('.move').on('click', (evt) => {
    evt.preventDefault();
    const entry = $(evt.target);
    const entry_id = {entry: entry.attr('id')};

    $.post('/move_entry', entry_id, (res) => {
        alert(res);
    });
    location.reload(true);
})

// Deletes entry from DB when delete button is clicked
$('.delete').on('click', (evt) => {
    evt.preventDefault();
    const entry = $(evt.target);
    const entry_id = {entry: entry.attr('id')};

    $.post('/delete_entry', entry_id, (res) => {
        alert(res);
    });
    location.reload(true);
});

// Show radio buttons with rating options when Add rating button is clicked
$('.edit-rating').on('click', (evt) => {
    evt.preventDefault();
    const entry = $(evt.target);
    const entry_id = entry.attr('id');
    $('.' + entry_id + '.rating').show();
    $('#' + entry_id + '.edit-rating').hide();
});

// Cancel updating rating and hide buttons without sending data
$('.cancel-rating').on('click', (evt) => {
    evt.preventDefault();
    const entry = $(evt.target);
    const entry_id = entry.attr('id');
    $('.' + entry_id + '.rating').hide();
    $('#' + entry_id + '.edit-rating').show();
});

// Update entry with rating value
$('.submit-rating').on('click', (evt) => {
    evt.preventDefault();
    const radioValue = $("input:checked").val();
    const entry = $(evt.target);
    const formData = {entry: entry.attr('id'), input: radioValue};

    
    $.post('/add_entry_rating', formData, (res) => {
        alert(res);

    });
    location.reload(true);
});


// Show textbox for adding note to entry
$('.edit-note').on('click', (evt) => {
    evt.preventDefault();

    const entry = $(evt.target);
    const entry_id = entry.attr('id');
    $('.' + entry_id + '.note').show();
    $('#' + entry_id + '.edit-note').hide();

});


// Cancel updating note and hide textbox without sending data
$('.cancel-note').on('click', (evt) => {
    evt.preventDefault();
    const entry = $(evt.target);
    const entry_id = entry.attr('id');
    $('.' + entry_id + '.note').hide();
    $('#' + entry_id + '.edit-note').show();
});

// Update entry with note value
$('.submit-note').on('click', (evt) => {
    evt.preventDefault();
    const entry = $(evt.target);
    const entry_id = entry.attr('id')
    const inputText = $('.note' + '.' + entry_id + '.text').val();
    const formData = {entry: entry_id, input: inputText};

    $.post('/add_entry_note', formData, (res) => {
        alert(res);

    });
    location.reload(true);
    
});

// On click of filter button, show filter options
$('#filter-button').on('click', (evt) => {
    evt.preventDefault();
    $('.rating-filter').show();
    
});

// On submit of filter for rating, send input to server and adjust roasters in list to be displayed
$('.rating-filter-submit').on('click', (evt) => {
    evt.preventDefault();
    const input = $('input:checked').val();

    const data = {rating: input};

    $.get('/filter', data, (res) => {
        $('.direct').html(res);

    });
});


// Trying to call photos through AJAX + jQuery - get CORS policy error
// $('.test').on('click', (evt) => {
//     evt.preventDefault();

//     const photo = $(evt.target).attr('id');
    
//     $.get('https://maps.googleapis.com/maps/api/place/photo?key=API_KEY&maxwidth=800&photoreference=' + photo, (res) => {
//         $().html(res);
//     });
// })


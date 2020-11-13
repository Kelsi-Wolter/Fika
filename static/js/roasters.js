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
    $('.edit-roaster-buttons').show();
    
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

// Update entry with note value
$('.submit-note').on('click', (evt) => {
    evt.preventDefault();
    const entry = $(evt.target);
    const entry_id = entry.attr('id')
    const inputText = $(".note" + '.' + entry_id).val();
 
    const formData = {entry: entry_id, input: inputText};
    
    $.post('/add_entry_note', formData, (res) => {
        alert(res);

    });
    location.reload(true);
    
});







// Add event listener to click on "create new list" button which redirects to /create_new_list

// document.getElementById("new-list-btn").onclick = function () {
//     location.href = '/create_new_list'  
//     // alert('Hey!');
// };
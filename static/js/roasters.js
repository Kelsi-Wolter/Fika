"use strict";

// Add event listener to click on "create new list" button which redirects to /create_new_list

// document.getElementById("new-list-btn").onclick = function () {
//     location.href = '/create_new_list'  
//     // alert('Hey!');
// };

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
    $('.edit-fav-buttons').show();
    
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
})

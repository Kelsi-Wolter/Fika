"use strict";

// Add event listener to click on "create new list" button which redirects to /create_new_list

// document.getElementById("new-list-btn").onclick = function () {
//     location.href = '/create_new_list'  
//     // alert('Hey!');
// };

$('.add-fav').on('click', (evt) =>{
    evt.preventDefault();
    const roaster = $(evt.target);
    const roaster_id = {roaster: roaster.attr('id')};
    // console.log(roaster_id);
    $.get('/add_to_fav_list', roaster_id, (res) => {
        alert(res);
    });
    
})


$('.add-roasters').on('click', (evt) =>{
    evt.preventDefault();
    const roaster = $(evt.target);
    const roaster_id = {roaster: roaster.attr('id')};
    // console.log(roaster_id);
    $.get('/add_to_roaster_list', roaster_id, (res) => {
        alert(res);
    });
    
})

$('.edit-fav').on('click', (evt) => {
    evt.preventDefault();
    $('.edit-fav-buttons').show();
    
});


// document.getElementById("add-fav").onclick = function () {
//     // create entry on favorites list with roaster and user
//     // flash message to user that roaster was added to list
//     // alert('Hey!');
// };

// document.getElementById("add-roast").onclick = function () {
//     // location.href = '/create_new_list' 
//     alert('Hey!');
// };
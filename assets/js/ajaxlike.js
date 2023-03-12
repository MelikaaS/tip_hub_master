/*jshint esversion: 6 */
/*globals $:false */
/*jshint -W069 */

function like(slug, id) {
    "use strict";
    var element = document.getElementById('like');
    var count = document.getElementById('count');
    $.get(`/like/${slug}/${id}`).then(response => {
        if(response['response'] === 'liked'){
            element.className="fa fa-heart";
            count.innerText = Number(count.innerText)+1;
        }else{
            element.className="fa fa-heart-o";
            count.innerText = Number(count.innerText)-1;
        }
    });


}
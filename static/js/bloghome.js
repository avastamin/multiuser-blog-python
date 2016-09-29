function setupDeletePost(blogid) {
    $('#deleteModal').modal('show');
    $('#blogid').val(blogid);
}

function deletePost() {
    var blogid = $('#blogid').val();
    $.ajax({
        method: "POST",
        url: "/blog/deletepost/" + blogid
    })
        .done(function () {
            $('div[id=' + blogid + ']').slideUp("slow");
            $('div[id=' + blogid + ']').remove();
            $('#deleteModal').modal('hide');

        })
        .fail(function (xhr) {
            console.log(('Request Status: ' + xhr.status + ' Status Text: ' + xhr.statusText + ' ' + xhr.responseText))
        });
}

function likeUnlikeHandler(blogid, username, todo) {

    $.ajax({
        method: "POST",
        url: "/like",
        dataType: 'json',
        data: JSON.stringify({ "blogid": blogid, "username": username, "todo": todo })
    })
        .done(function (data) {
            console.log("enterd");
            var likeid = blogid + "likes";
            var heartid = blogid + "heart";
            var buttonid = blogid + "button";
            //console.log(data)
            $("span[id=" + likeid + "]").text(data['likes']);
            //alert(heartid);
            // toggle class to show right heart (filled/empty)
            console.log("span[id = '" + heartid + "']");
            $("span[id = '" + heartid + "']").toggleClass('glyphicon-heart-empty');
            $("span[id = '" + heartid + "']").toggleClass('glyphicon-heart');
            // change the onclick handler to call the other todo next time - like vs. unlike
            if (todo == "like")
                todo = "unlike";
            else
                todo = "like";

            console.log("likeUnlikeHandler('" + blogid + "','" + username + "','" + todo + "')");
            $("button[id=" + buttonid + "]").attr("onclick", "likeUnlikeHandler('" + blogid + "','" + username + "','" + todo + "')");
            //$ ("button[id=" +buttonid+ "]" ).click(likeUnlikeHandler(blogid, username, todo));
        })
        .fail(function (xhr) {
            console.log(('Request Status: ' + xhr.status + ' Status Text: ' + xhr.statusText + ' ' + xhr.responseText))
        })
        ;
}

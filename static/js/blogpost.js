function setupDeletePost(blogid) {
    $('#deleteModal').modal('show');
    $('#blogid').val(blogid);
}

function deletePost() {
    var blogid = $('#blogid').val();
    $.ajax({
        method: "POST",
        url: "/blog/deletepost/" + blogid,
        dataType: 'json',
        data: JSON.stringify({ 'origin': 'postpage' })
    })
        .done(function () {
            console.log("deleted, you would hope");
            $('#deleteModal').modal('hide');
            setTimeout(function () {
                window.location = "/blog";
            }, 1000)

        })
        .fail(function (xhr) {
            console.log(('Request Status: ' + xhr.status + ' Status Text: ' + xhr.statusText + ' ' + xhr.responseText))
        });
}

function saveEdit() {

    $.ajax({
        method: "POST",
        url: "/commentedit",
        dataType: 'json',
        data: JSON.stringify({ 'commentid': $('#editcommentid').val(), "updatedcomment": $('#delCommentTA').val() })
    })
        .done(function (data) {
            // show the updated text in the comment
            var commentp = $('#editcommentid').val() + "text";
            $('p[id=' + commentp + ']').html($('#delCommentTA').val());
            // show the updated time
            var timediv = $('#editcommentid').val() + "added";
            $('div[id=' + timediv + ']').html(data['added']);
            // Move this comment to the top since it is the latest
            var commentwell = $('#editcommentid').val() + "comments";
            $('div[id=' + commentwell + ']').prependTo($('#comments'));

            $('#editCommentModal').modal('hide');
        })
        .fail(function (xhr) {
            console.log(('Request Status: ' + xhr.status + ' Status Text: ' + xhr.statusText + ' ' + xhr.responseText));
        });

}

function setupEditComment(commentid) {
    var textid = commentid+'text';
    var commenttext = $('p[id='+textid+']').html();
    $('#delCommentTA').val(commenttext);
    $('#editcommentid').val(commentid);
    $('#editCommentModal').modal('show');
}

function deleteComment() {
    $.ajax({
        method: "POST",
        url: "/commentdelete",
        dataType: 'json',
        data: JSON.stringify({ 'commentid': $('#commentid').val() })
    })
        .done(function (data) {
            var commentid = $('#commentid').val() + "comments";
            $('div[id=' + commentid + ']').slideUp("slow");
            $('div[id=' + commentid + ']').remove();
            $('#deleteCommentModal').modal('hide');
            var countid = data['blogid'] + "comments";
            $('span[id=' + countid + ']').text(data['commentsnum']);

        })
        .fail(function (xhr) {
            console.log(('Request Status: ' + xhr.status + ' Status Text: ' + xhr.statusText + ' ' + xhr.responseText));
        });

}
function setupDelComment(commentid) {

    $('#commentid').val(commentid);
    $('#deleteCommentModal').modal('show');
}




function buildCommentHTML(username, added, commenttext, blogid, commentid) {
    var qcommentid = "'" + commentid + "'";
    var qcommenttext = "'" + commenttext + "'";
    var newcomment = '<div class="well" id="';
    newcomment += commentid;
    newcomment += 'comments"><div class="row"><div class="col-xs-6">';
    newcomment += username;
    newcomment += ' says:</div><div class="col-xs-6 text-right id="';
    newcomment += commentid;
    newcomment += "added'>";
    newcomment += added;
    newcomment += '</div> </div>  <div class="row"><div class="col-xs-12"><p class="data" id="';
    newcomment += commentid;
    newcomment += 'text">';
    newcomment += commenttext;
    newcomment += '</p> </div>  </div><div class="row"><div class="col-xs-2">';

    newcomment += '<button type="button"  class="btn btn-default" aria-label="Left Align"  onclick="setupEditComment(';

    newcomment += qcommentid;
    newcomment += ')"';
    newcomment += '><span class="glyphicon glyphicon-edit" aria-hidden="true"></span></button> ';


    newcomment += '<button type="button" class="btn btn-default" aria-label="Left Align" ';
    newcomment += 'onclick="setupDelComment(';
    newcomment += qcommentid;
    newcomment += ')"';
    newcomment += '><span class="glyphicon glyphicon-trash" aria-hidden="true"></span></button>  </div></div></div>';

    return newcomment;
}

function commentHandler(blogid, username) {
    var commenttext = $('#commentbox').val();
    if (commenttext && commenttext.length > 0) {
        $.ajax({
            method: "POST",
            url: "/comment",
            dataType: 'json',
            data: JSON.stringify({ "blogid": blogid, "username": username, "comment": commenttext })
        })
            .done(function (data) {
                console.log("if block");
                var added = data["added"];
                var commentid = data["commentid"];
                console.log(added);
                var newcomment = buildCommentHTML(username, added, commenttext, blogid, commentid);
                console.log("AGAIN --- " + newcomment);
                var ccount = blogid + "comments";
                $('#comments').hide();
                $('#comments').prepend(newcomment);
                $('#comments').slideDown("slow");
                $("span[id=" + ccount + "]").text(data['comments']);
                $('#commentbox').val('');
            })
            .fail(function (xhr) {
                console.log(('Request Status: ' + xhr.status + ' Status Text: ' + xhr.statusText + ' ' + xhr.responseText));
            });
    }
    else {
        alert("Please enter a comment before posting!");
    }
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
            $("span[id=" + likeid + "]").text(data['likes']);
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
        })
        .fail(function (xhr) {
            console.log(('Request Status: ' + xhr.status + ' Status Text: ' + xhr.statusText + ' ' + xhr.responseText));
        })
        ;
}
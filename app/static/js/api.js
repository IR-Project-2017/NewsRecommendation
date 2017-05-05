function updateLike(index) {
    $like = $("#like" + index)
    var id = $like.data("id");
    var title = $like.data("title");
    $.ajax({
        type: "POST",
        url: "/api/like",
        data: {"title": title,
                "id": id}
    })
    .done(function(){
        console.log("success");
        $like.removeClass("like_btn")
        $like.addClass("pushed")
    })
    .fail(function(){
        console.log("fail");
    });
}

function updateDislike(index) {
    $dislike = $("#dislike" + index)
    var id = $dislike.data("id");
    var title = $dislike.data("title");
    console.log(index)
    $.ajax({
        type: "POST",
        url: "/api/dislike",
        data: {"title": title,
                "id": id}
    })
    .done(function(){
        console.log("success");
        $dislike.removeClass("like_btn")
        $dislike.addClass("pushed")
    })
    .fail(function(){
        console.log("fail");
    });
}
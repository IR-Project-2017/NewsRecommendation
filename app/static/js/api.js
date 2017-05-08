function updateLike(index) {
    $like = $("#like" + index)
    var id = $like.data("id");
    var title = $like.data("title");
    var doc_type = $like.data("doc_type");
    console.log(doc_type)
    $.ajax({
        type: "POST",
        url: "/api/like",
        data: {"title": title,
                "doc_type": doc_type,
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
    var doc_type = $dislike.data("doc_type");
    $.ajax({
        type: "POST",
        url: "/api/dislike",
        data: {"title": title,
                "doc_type": doc_type,
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

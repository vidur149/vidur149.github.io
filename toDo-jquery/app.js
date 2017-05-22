$(function() {
    var task = {};
    $.get({
        url: "http://localhost:5000/tasks",
        success: success,
    });

    function success(result) {
        var tasks = result['tasks'];
        $.each(tasks, function(key, value) {
            $("#list").append("<li data-id='" + value['id'] + "'><div class='title'>" + value["title"] + "</div><div data-id='" + value['id'] + "'class='remove'>X</div></li>");
        });
    }

    $("body").on("click", "div.remove", function() {
        var id = $(this).attr("data-id");
        $.ajax({
            method: 'DELETE',
            url: "http://localhost:5000/tasks/" + id,
            success: function(result) { $("li[data-id='" + id + "'").remove(); },
        });

    });


    $("form").on("submit", function(event) {
        event.preventDefault();
        var formArray = $(this).serializeArray();
        var jsObj = {
            title: formArray[0]['value']
        }
        var jsonObj = JSON.stringify(jsObj);
        console.log(jsonObj);
        $.post({
            url: "http://localhost:5000/tasks",
            contentType: "application/json; charset=utf-8",
            data: jsonObj,
            dataType: 'json',
            crossDomain: true,
            success: function(result) {
                var task = result['task'];
                // console.log(tasks);
                $("#list").append("<li><div class='title'>" + task["title"] + "</div><div data-id='" + task['id'] + "'class='remove'>X</div></li>");
                $("form").trigger("reset");
            }
        });
    });
});
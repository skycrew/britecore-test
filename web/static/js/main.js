$(document).ready(function() {
    $("#frTargetDate").datepicker({ format: "yyyy-mm-dd" });
    $("#frTargetDateEdit").datepicker({ format: "yyyy-mm-dd" });

    $("#addBtn, .editBtn").click(function() {
        $(".error-placeholder").hide();
    });

    $(".editBtn").click(function() {
        var frId = $(this).data("edit");

        $.get("/edit/" + frId, function(data) {
            $("#frTitleEdit").val(data.title);
            $("#frDescriptionEdit").val(data.description);
            $("#frClientEdit").val(data.clientId);
            $("#frPriorityEdit").val(data.priority);
            $("#frTargetDateEdit").val(data.targetDate);
            $("#frProductEdit").val(data.productId);
            $("#frIdEdit").val(frId);
        });
    });

    $("#saveAdd").click(function() {
        $.ajax({
            type: "post",
            url: "/add",
            data: $("#addForm").serialize(),
            success: function(data) {
                if (data.errors) {
                    $(".error-placeholder").html(data.errors.join("<br>")).show();
                    $("#frTitle").focus();
                }
                if (data.url) { location.reload() }
            },
            error: function() {
                alert("Oopss! Something went wrong.");
            }
        });
    });

    $("#saveEdit").click(function() {
        $.ajax({
            type: "post",
            url: "/edit/" + $("#frIdEdit").val(),
            data: $("#editForm").serialize(),
            success: function(data) {
                if (data.errors) {
                    $(".error-placeholder").html(data.errors.join("<br>")).show();
                    $("#frTitle").focus();
                }
                if (data.url) { location.reload() }
            },
            error: function() {
                alert("Oopss! Something went wrong.");
            }
        });
    });

    // Ctrl + Shift + O --> Add new feature request
    $(document).bind("keydown", function(e) {
        if (e.ctrlKey && e.shiftKey && e.which === 79) {
            e.preventDefault();
            $("#addBtn").click();
            return false;
        }
    });

    // Ctrl + Shift + S --> Save
    $(document).bind("keydown", function(e) {
        if (e.ctrlKey && e.shiftKey && e.which === 83) {
            e.preventDefault();

            if ($("#addForm").is(":visible")) {
                $("#saveAdd").click();
            }

            if ($("#editForm").is(":visible")) {
                $("#saveEdit").click();
            }

            return false;
        }
    });
});

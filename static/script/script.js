$("#file-upload").val('');
            $("#compare").addClass('hide');

            $("#start").submit(function(e) {
                e.preventDefault(); // avoid to execute the actual submit of the form.
                var form = $(this)
                var formdata = new FormData(form[0]);
                var formAction = form.attr('action');
                
                if (!$("#file-upload").val()){
                    $("#import-img").css('color', 'red');
                    $("#error-message").empty();
                    $("#error-message").append(
                        '<div class="alert alert-danger mt-2" role="alert">Img upload is required!</div>'
                    );
                    return
                } else {
                    $("#import-img").css('color', 'black');
                    $("#error-message").empty();
                }

                $("#start-button").text("Loading...");
                $("#start-button").prop('disabled', true);

                $.ajax({
                    url         : formAction,
                    data        : formdata ? formdata : form.serialize(),
                    cache       : false,
                    contentType : false,
                    processData : false,
                    type        : 'POST',
                    success     : function(data, textStatus, jqXHR){
                        if (data['status'] == "ERROR"){
                            $("#start-button").text("Start");
                            $("#start-button").prop('disabled', false);
                            $("#error-message").append(`<div class="alert alert-danger mt-2" role="alert">${data['error']}: ${data['error_msg']}</div>`);
                        } else {
                            $("#raster").attr('src', data['raster']);
                            $("#vector").empty();
                            $("#vector").append(data['vector']);
                            $("#start-button").text("Start");
                            $("#start-button").prop('disabled', false);
                            $("#compare").removeClass('hide');
                        }
                    }
                });
            

            });

            function uploadFile(target) {
                var fn = target.files[0].name;
                $("#import-img").text("");
                $("#import-img").append("You uploaded -> " + fn + "<br>Click again to upload another file!");
            }
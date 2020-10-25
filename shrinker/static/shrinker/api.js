$(document).ready(function() {
    csrftoken = $(this).find('[name="csrfmiddlewaretoken"]').val();
    let is_submiting = false;
    let domain = $("#url_form").data("domen") + '/';
    let current_page = 0;
    let page_size = 10;
    let api_url = $('#url_form').attr('action');
    let paginator = $('.paginator-object').detach();

    $('#id_edit_new').bind('change', function (event) {
        if ($(this).val() == 'auto') {
            $('#id_url_new').parent().addClass("d-none");
            $('#id_url_new').val("");
        } else {
            $('#id_url_new').parent().removeClass("d-none");
        }
    });
    $('#id_edit_new').trigger("change");

    function copy_previous_link(event){
       event.preventDefault();
       copyTextToClipboard($(this).attr("href"));
    }

    function hide_messages() {
        $('#url_form .text-danger').remove();
        $('#url_form .border-danger').removeClass("border-danger");
        $(".url-info.d-block").remove();
    }

    function delete_url(event) {
        event.preventDefault();
        let data = {
            'csrfmiddlewaretoken': csrftoken
        };
        $.ajax({
            type: "DELETE",
            url: $(this).attr("href"),
            success: function (response) {
                console.log(response);
                refresh_url_list();
            },
            error: function( jqXHR , textStatus, errorThrown) {
                console.log("error");
            },
            complete: function (xhr, textStatus) {
            }
        });

    }

    function add_redirect_url(redirect_data) {
        let new_message = $(".url-info.d-none").clone();
        new_message.addClass("d-block").addClass("alert-success").removeClass("d-none");
        new_message.find('.created_url_original').attr("href", redirect_data.url_original);
        new_message.find('.created_url_original').html(redirect_data.url_original);
        new_message.find('.created_url_new').attr("href", domain + redirect_data.url_new);
        new_message.find('.created_url_new').html(domain + redirect_data.url_new);
        $(".url-info.d-none").after(new_message);
        new_message.find(".copy-url").attr("href", domain + redirect_data.url_new);
        new_message.find(".copy-url").bind('click', copy_previous_link);
    }

    function select_page(event) {
        event.preventDefault();
        current_page = $(this).data("page");
        refresh_url_list();
    }

    function create_paginator(count) {
        $('#top-paginator-container nav').remove();
        if (count < 0) return;
        let page_count = Math.floor(count / page_size);
        let new_paginator = paginator.clone();
        if (current_page === 0) {
            new_paginator.find(".pagination-prev").addClass("disabled");
        }
        if (current_page === page_count) {
            new_paginator.find(".pagination-next").addClass("disabled");
        }
        new_paginator.find(".pagination-prev a").data("page", current_page - 1);
        new_paginator.find(".pagination-next a").data("page", current_page + 1);
        for (let i = 0; i <= page_count; i++) {
            let page_url = $('<a>', {
                class: "page-link",
                href: "#",
                data: {page: i},
                html: (i + 1)
            });
            let li = $('<li>', {
                class: i === current_page ? "page-item active" : "page-item"

            });
            li.append(page_url);
            new_paginator.find("li.pagination-next").before(li);
        }
        $('#top-paginator-container').append(new_paginator);
        new_paginator.find("a").bind("click", select_page);
    }

    function show_urls(url_list) {
        if (url_list.length == 0) {
            $('#created-url-list').addClass('d-none');
        } else {
            $('#created-url-list').removeClass('d-none');
        }
        $('#created-url-list tbody tr').remove();
        for (let i=0; i< url_list.length; i ++) {
            let tr = $('<tr>');
            tr.append($('<td>', {
                html: url_list[i].url_original
            }));
            tr.append($('<td>', {
                html: '<a target="_blank" href="'+domain + url_list[i].url_new+'">'+domain + url_list[i].url_new+'</a>',
            }));
            tr.append($('<td>', {
                html: '<a class="copy-url" href="'+domain + url_list[i].url_new+'">(copy)</a>',
            }));
            tr.append($('<td>', {
                html: '<a class="delete-url" href="'+api_url+url_list[i].pk+'">(del)</a>'
            }));
            console.log(tr)
            $('#created-url-list tbody').append(tr);
        }
            $('#created-url-list tbody .copy-url').bind('click', copy_previous_link);
            $('#created-url-list tbody .delete-url').bind('click', delete_url);
    }
    function refresh_url_list() {
        $.ajax({
            type: "GET",
            url: api_url + "?limit="+page_size+"&offset=" + (current_page * page_size),
            success: function (response) {
                console.log(response);
                create_paginator(response.count - 1);
                show_urls(response.results);
            },
            error: function( jqXHR , textStatus, errorThrown) {
                console.log("error");
            },
            complete: function (xhr, textStatus) {
            },
            dataType: "json"
        });
    }

    $('#url_form').bind("submit", function (event) {
        event.preventDefault();
        if (is_submiting) return;  // блокируем отправку следующего запроса, пока не получим результат последнего
        hide_messages();
        is_submiting = true;

        //let csrftoken = $(this).find('[name="csrfmiddlewaretoken"]').val();
        let data = {
            'url_original': $("#id_url_original").val(),
            'url_new': $("#id_url_new").val().replace(domain, ""),
            //'csrfmiddlewaretoken': csrftoken
        };
        $.ajax({
            type: "POST",
            url: api_url,
            data: data,
            success: function (redirect_data) {
                $('#id_url_original').val("");
                add_redirect_url(redirect_data);
                refresh_url_list();
            },
            error: function( jqXHR , textStatus, errorThrown) {
                $.each(jqXHR.responseJSON, function(field_name, error_list) {
                    console.log(field_name, error_list);
                    $('#id_'+field_name).addClass("border-danger");
                    for (let i=0; i < error_list.length; i++) {
                        $('#id_'+field_name).after($("<span>", {
                            class: "text-danger",
                            html: error_list[i]
                        }));
                    }
                });
            },
            complete: function (xhr, textStatus) {
                is_submiting = false;
            },
            dataType: "json"
        });
    });

    refresh_url_list();
});
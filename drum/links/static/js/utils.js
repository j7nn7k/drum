$(document).ready(function () {
    var $linkField = $("#id_link");
    $linkField.on("input", function () {
        var url = $linkField.val();
        var urlEncoded = encodeURIComponent(url);
        var domainOfLink = links.extractDomain(url);

        if (links.isUrlValid(url)) {
            $.get("/proxy?url=" + urlEncoded, function () {
                })
                .done(function (data) {
                    var socialImagePath = "";
                    $.each($(data), function (index, value) {
                        socialImagePath = links.getSocialImage(value);
                        if (socialImagePath) {
                            if (socialImagePath.indexOf("//") < 0) {
                                socialImagePath = domainOfLink + socialImagePath;
                            }
                            return false;
                        }
                    });

                    $("#id_main_image").val(socialImagePath);
                    $("#id_main_image").trigger("input");
                })
                .fail(function () {
                    console.log("No og:image found");
                })
                .always(function () {
                });
        }
    });

    var $mainImageField = $("#id_main_image");
    $mainImageField.on("input", function () {
        $(".main-image-preview").attr("src", $("#id_main_image").val());
    });

    var simplemde = new SimpleMDE({
        element: $("#id_description")[0],
        spellChecker: false,
        toolbar: ["bold", "italic", "unordered-list", "ordered-list", "heading-2", "heading-3", "link", "|", "preview", "|", "guide"]
    });
});

var links = {
    isUrlValid: function (url) {
        return /^(https?|s?ftp):\/\/(((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:)*@)?(((\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5]))|((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.?)(:\d*)?)(\/((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)+(\/(([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)*)*)?)?(\?((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)|[\uE000-\uF8FF]|\/|\?)*)?(#((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)|\/|\?)*)?$/i.test(url);
    },
    getSocialImage: function (value) {
        var imgPath;
        if (value.tagName == "meta" || value.tagName == "META") {
            if (
                value.attributes.property && value.attributes.property.value == "og:image" ||
                value.attributes.name && value.attributes.name.value == "twitter:image:src" ||
                value.attributes.itemprop && value.attributes.itemprop.value == "image") {
                imgPath = value.content;
            }
        }
        return imgPath;
    },
    extractDomain: function (url) {
        var domain;
        var protocol;
        //find & remove protocol (http, ftp, etc.) and get domain
        if (url.indexOf("://") > -1) {
            protocol = url.split("://")[0] + "://";
            domain = url.split("/")[2];
        }
        else {
            domain = url.split("/")[0];
        }
        //find & remove port number
        domain = domain.split(":")[0];

        return protocol + domain;
    }
};
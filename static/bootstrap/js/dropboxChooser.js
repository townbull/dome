/**
 * Created by zhu on 3/16/14.
 */
$(function(){
            var options = {

    // Required. Called when a user selects an item in the Chooser.
    success: function(files) {

        var jsonString = JSON.stringify(files);
        $.ajax({
            url: "dropbox/save",
            data: {'source':'dropbox', 'files':jsonString, 'userId':{{ user.id }}},
            type: "POST"

        }).done(function(){
            location.reload();
        });
    },

    // Optional. Called when the user closes the dialog without selecting a file
    // and does not include any parameters.
    cancel: function() {

    },

    // Optional. "preview" (default) is a preview link to the document for sharing,
    // "direct" is an expiring link to download the contents of the file. For more
    // information about link types, see Link types below.
    linkType: "preview", // or "direct"

    // Optional. A value of false (default) limits selection to a single file, while
    // true enables multiple file selection.
    multiselect: true, // or true

    // Optional. This is a list of file extensions. If specified, the user will
    // only be able to select files with these extensions. You may also specify
    // file types, such as "video" or "images" in the list. For more information,
    // see File types below. By default, all extensions are allowed.
    extensions: ['.pdf', '.doc', '.docx', '.txt']
};
            var button = Dropbox.createChooseButton(options);
            document.getElementById("container").appendChild(button);

        });

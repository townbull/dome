/**
 * Created by zhu on 3/16/14.
 */

      //var pickerApiLoaded;
      //var pickerCreated = false;
      var authorized;
      var picker;
      var oauthToken;


      function onApiLoad(appId,accountId ) {
         //pickerApiLoaded = false;
          authorized = false;
         $.ajax({
            url: "gettoken",
            data: {'appId':appId, 'accountId':accountId},
            type: "POST"
            }).done(function(data){
                oauthToken = data["token"];
             //oauthToken="ya29.1.AADtN_VpYYA6TWxCCkGtHp-D8VTIxt18Wtzj6VqcaXstKxss2Xilf2uDfkYm0H_pwguOQA";
                alert("oauthToken:"+oauthToken);
             authorized = true;
             //gapi.load('picker', {'callback': onPickerApiLoad});
             gapi.load('picker', {'callback': createPicker});
            });
      }



//      function onPickerApiLoad() {
//        pickerApiLoaded = true;
//          if (!pickerCreated)
//            createPicker();
//          else
//            picker.setVisible(true);
//      }


      // Create and render a Picker object
      function createPicker() {
        //if (pickerApiLoaded && oauthToken) {
          if (oauthToken) {
              picker = new google.picker.PickerBuilder().
              addView(google.picker.ViewId.DOCS).
              enableFeature(google.picker.Feature.MULTISELECT_ENABLED).
              setOAuthToken(oauthToken).
              //setDeveloperKey(developerKey).
              setCallback(pickerCallback).
              build();
          //pickerCreated = true;
          picker.setVisible(true);
        }
      }


      function pickerCallback(data) {
        if (data[google.picker.Response.ACTION] == google.picker.Action.PICKED) {
            var jsonString = JSON.stringify(data[google.picker.Response.DOCUMENTS]);
          $.ajax({
            url: "googleDrive/save",
            data: {'source':'googleDrive', 'files':jsonString,  'userId':{{ user.id }}},
            type: "POST"

        }).done(function(){
            location.reload();
        });

        }

      }

$(function() {

    $( "body" ).on( "click", ".compare", function() {
        var $screenshot = $( this ).parents( ".result" ).find( ".screenshot" );
        reset( $screenshot );
        diff( $screenshot );
    }).on( "click", ".compare-all", function() {
        resetAll();
        diffAll();
    });

    function complete( data, $screenshot ) {
        var $result = $screenshot.parents( ".result" )
        $result.find( ".mismatch-percentage" ).text( data.misMatchPercentage );

        var diffImage = new Image();
        diffImage.src = data.getImageDataUrl();
        $result.find( ".diff" ).html( diffImage );
    }

    function diffAll() {
        $( ".screenshot" ).each( function() {
            diff( $( this ) );
        });
    }

    function diff( $screenshot ) {
        var mock = $screenshot.parents( ".test" ).find( ".mock" ).attr( "src" ),
            prod = $screenshot.attr( "src" ),
            onComplete = function( data ) { complete( data, $screenshot ); };

        resemble( mock ).compareTo( prod ).onComplete( onComplete );
    }

    function reset( $screenshot ) {
        var $result = $screenshot.parents( ".result" );
        $result.find( ".mismatch-percentage" ).html( "&hellip;" );
        $result.find( ".diff" ).empty();
    }

    function resetAll() {
        $( ".mismatch-percentage" ).html( "&hellip;" );
        $( ".diff" ).empty();
    }

    resemble.outputSettings({
        largeImageThreshold: 0
    });

    diffAll();

    function getBase64Image(img) {

        // Create an empty canvas element
        var canvas = document.createElement("canvas");
        canvas.width = img.width;
        canvas.height = img.height;

        // Copy the image contents to the canvas
        var ctx = canvas.getContext("2d");
        ctx.drawImage(img, 0, 0);

        // Get the data-URL formatted image
        // Firefox supports PNG and JPEG. You could check img.src to
        // guess the original format, but be aware the using "image/jpg"
        // will re-encode the image.
        var dataURL = canvas.toDataURL("image/png");

        return dataURL.replace(/^data:image\/(png|jpg);base64,/, "");
    }

    function getBase64FromImageUrl(URL) {
        var img = new Image();
        img.src = URL;
        img.onload = function() {

            var canvas = document.createElement("canvas");
            canvas.width = this.width;
            canvas.height = this.height;

            var ctx = canvas.getContext("2d");
            ctx.drawImage(this, 0, 0);

            var dataURL = canvas.toDataURL("image/png");

            return dataURL.replace(/^data:image\/(png|jpg);base64,/, "");

        };
    }

});

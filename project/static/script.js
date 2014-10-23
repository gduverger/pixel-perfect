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

        console.log( mock, prod );
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
        largeImageThreshold: 999999
    });

    diffAll();

});

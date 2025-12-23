<script>
// Extract the fragment from the URL
var fragment = window.location.hash.substring(1);

var oldUrl = new URL(window.location.href);

if (fragment) {
    // Set the fragment as a query parameter
    var newUrl = new URL(oldUrl.origin + oldUrl.pathname);

    fragment.split("&").forEach((param) => {
        var [param_key, param_value] = param.split("=");

        newUrl.searchParams.set(param_key, param_value);
    });

    window.history.replaceState({}, '', newUrl.toString());
}
</script>
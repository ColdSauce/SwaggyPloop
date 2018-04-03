$(function () {
    const entityMap = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#39;',
        '/': '&#x2F;',
        '`': '&#x60;',
        '=': '&#x3D;'
    };

    // The following code is from a Stackoverflow answer on escaping HTML to mitigate XSS
    // https://stackoverflow.com/questions/24816/escaping-html-strings-with-jquery
    function escapeHtml(string) {
        return String(string).replace(/[&<>"'`=\/]/g, function (s) {
            return entityMap[s];
        });
    }

    /**
     * getInfectedHosts queries the API to get all the current infected hosts' MAC addresses.
     */
    async function getInfectedHosts() {
        const ajaxCall = await $.ajax({
            url: "/get_infected_hosts",
            cache: false
        });
        return JSON.parse(ajaxCall).map(escapeHtml);
    }

    /**
     * getPayloads queries the API to get all of the payloads a given MAC address sent.
     * @param {string} macAddress MAC address one would like to get payloads from.
     */
    async function getPayloads(macAddress) {
        const ajaxCall = await $.ajax({
            url: "/get_payloads?mac_address=" + macAddress,
            cache: false
        });
        return JSON.parse(ajaxCall).map((payload) => {
            return {
                name: escapeHtml(payload.name),
                payload_id: escapeHtml(payload.payload_id)
            };
        });
    }

    /**
     * getPayload queries the API to get a specific payload
     * @param {string} macAddress the infected host's MAC address to get payload from.
     * @param {string} payloadId specific payload's identifier.
     */
    async function getPayload(macAddress, payloadId) {
        const ajaxCall = await $.ajax({
            url: "/get_payload?mac_address=" + macAddress + "&payload_id=" + payloadId,
            cache: false
        });
        return escapeHtml(ajaxCall);
    }

    // This toggle main state variable is used to be able to perform complete cascading `display:none` even when some
    // children nodes are already hidden.
    var toggledMainState = 0;

    /**
     * toggleVisibility switches the CSS styling of a JQuery element from display: block to display: none and vice versa
     * @param {JQuery Element} someElement the element one would like to set visible or not visible
     * @param {boolean} shouldUseMainState whether the visibility should be viewed from a macro level vs a micro level
     */
    function toggleVisibility(someElement, shouldUseMainState) {
        if (shouldUseMainState === 1) {
            if (toggledMainState === 0) {
                someElement.css('display', 'block');
                toggledMainState = 1;
            } else {
                someElement.css('display', 'none');
                toggledMainState = 0;
            }
            return;
        }
        if (someElement.css('display') === 'none') {
            someElement.css('display', 'block');
        } else if (someElement.css('display') === 'block') {
            someElement.css('display', 'none');
        }
    }

    /**
     * toggleChildrenVisibility toggles the current node's visibility and also all of its children's visibility.
     * it is to be used within a JQuery context as it uses an implicit `$(this)`.
     */
    function toggleChildrenVisibility() {
        toggleVisibility($(this));
        const children = $(this).children();
        children.each(function () {
            toggleVisibility($(this), 1);
        });
    }

    /**
     * createHostLink creates the JQuery element that defines the view and implementation of an infected host's anchor tag link. 
     * @param {string} host The MAC Address of an infected host.
     */
    function createHostLink(host) {
        const hostLink = $("<a>");

        hostLink.append(host);
        hostLink.attr("href", "#");
        hostLink.addClass("host_link");

        hostLink.click(function () {
            $(this).siblings().each(toggleChildrenVisibility);
            return false;
        });
        return hostLink;
    }

    /**
     * createHostDiv creates the JQuery element used for storing the hosts
     */
    function createHostDiv() {
        const hostDiv = $("<div>");
        hostDiv.addClass("host_name");
        return hostDiv;
    }

    /**
     * createUserPayloadsDiv creates the JQuery element used for storing user payloads
     */
    function createUserPayloadsDiv() {
        const userPayloadsDiv = $("<div>");
        userPayloadsDiv.addClass("user_payloads");
        return userPayloadsDiv;
    }

    /**
     * createUserPayloadsLink creates the JQuery element that defines the view and implementation of an payload's anchor tag link. 
     * @param {string} payload the payload one would like to base the link around.
     */
    function createUserPayloadsLink(payload) {
        const userPayloadsLink = $("<div>");
        userPayloadsLink.append("Name: ");

        const userPayloadsLinkAnchor = $("<a>");
        userPayloadsLinkAnchor.attr("href", "#");
        userPayloadsLinkAnchor.addClass("payload_name_link");
        userPayloadsLinkAnchor.append(payload['name']);

        userPayloadsLink.append(userPayloadsLinkAnchor);
        userPayloadsLink.click(function () {
            $(this).closest('.user_payloads').siblings().each(function () {
                toggleVisibility($(this));
            });
            return false;
        });
        return userPayloadsLink;
    }

    /**
     * createUI gets the infected hosts along with their payloads and renders the information.
     */
    async function createUI() {
        const infectedHosts = await getInfectedHosts();
        infectedHosts.forEach(async (host) => {
            const payloads = await getPayloads(host);

            const hostDiv = createHostDiv();
            const hostLink = createHostLink(host);

            hostDiv.append(hostLink);
            $("#infected_hosts").append(hostDiv);

            payloads.forEach(async (payloadObject) => {
                const userPayloadsDiv = createUserPayloadsDiv();
                const userPayloadsLink = createUserPayloadsLink(payloadObject);

                userPayloadsDiv.append(userPayloadsLink);

                const payload = await getPayload(host, payloadObject['payload_id']);

                const payloadDataDiv = $("<pre class=\"payload\"></pre>");
                payloadDataDiv.append(payload);
                const containerDiv = $("<div class=\"container\"></div>");
                containerDiv.css("display", "none");
                containerDiv.append(userPayloadsDiv);
                containerDiv.append(payloadDataDiv);
                hostDiv.append(containerDiv);
            });
        });
    }

    // Call the createUI function to render the UI.
    (async function () {
        await createUI();
    })();
});
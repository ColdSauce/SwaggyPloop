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

    // The following code was borrowed from a Stackoverflow answer on escaping HTML to mitigate XSS
    // https://stackoverflow.com/questions/24816/escaping-html-strings-with-jquery
    function escapeHtml (string) {
        return String(string).replace(/[&<>"'`=\/]/g, function (s) {
            return entityMap[s];
        });
    }

    async function getInfectedHosts() {
        const ajaxCall = await $.ajax({
            url: "/get_infected_hosts",
            cache: false
        });
        return JSON.parse(ajaxCall).map(escapeHtml);
    }

    async function getPayloads(macAddress) {
        const ajaxCall = await $.ajax({
            url: "/get_payloads?mac_address=" + macAddress,
            cache: false
        })
        return JSON.parse(ajaxCall).map((payload) => {
            return {
                name: escapeHtml(payload.name),
                payload_id: escapeHtml(payload.payload_id)
            };
        });
    }

    async function getPayload(macAddress, payloadId) {
        const ajaxCall = await $.ajax({
            url: "/get_payload?mac_address=" + macAddress + "&payload_id=" + payloadId,
            cache: false
        });
        return escapeHtml(ajaxCall);
    }

    var toggledMainState = 0;

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

    function toggleChildrenVisibility() {
        toggleVisibility($(this));
        const children = $(this).children();
        children.each(function () {
            toggleVisibility($(this), 1);
        });
    }

    function createHostLink(host) {
        const hostLink = $("<a>");

        hostLink.append(host)
        hostLink.attr("href", "#");
        hostLink.addClass("host_link");

        hostLink.click(function () {
            $(this).siblings().each(toggleChildrenVisibility);
            return false;
        });

        return hostLink;
    }

    function createHostDiv() {
        const hostDiv = $("<div>");
        hostDiv.addClass("host_name");
        return hostDiv;
    }

    function createUserPayloadsDiv() {
        const userPayloadsDiv = $("<div>");
        userPayloadsDiv.addClass("user_payloads");
        return userPayloadsDiv;
    }

    function createUserPayloadsLink(payload) {
        const userPayloadsLink = $("<div>");
        userPayloadsLink.append("Name: ");

        const userPayloadsLinkAnchor  = $("<a>");
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
    };

    (async function() {
        await createUI();
    })();
});
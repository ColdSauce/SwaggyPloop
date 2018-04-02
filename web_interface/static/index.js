console.log("hello world");

$(function () {


    const getInfectedHosts = (cb) => {
        return $.ajax({
            url: "/get_infected_hosts",
            cache: false,
            success: (j) => cb(JSON.parse(j))
        });
    }

    const getPayloads = (macAddress, cb) => {
        return $.ajax({
            url: "/get_payloads?mac_address=" + macAddress,
            cache: false,
            success: (j) => cb(JSON.parse(j))
        });
    }

    const getPayload = (macAddress, payloadId, cb) => {
        return $.ajax({
            url: "/get_payload?mac_address=" + macAddress + "&payload_id=" + payloadId,
            cache: false,
            success: cb
        });
    }

    function toggleSiblingVisibility() {
        const sibling = $(this);
        if (sibling.css('display') === 'none') {
            sibling.css('display', 'block');
        } else {
            sibling.css('display', 'none');
        }
    }


    getInfectedHosts((hosts) => {
        hosts.forEach((host) => {
            getPayloads(host, (payloads) => {
                const hostDiv = $("<div class=\"host_name\"> </div>");
                const hostLink = $("<a href=\"#\" class=\"host_link\">" + host + "</a>");
                hostLink.click(function () {
                    $(this).siblings().each(toggleSiblingVisibility);
                });
                hostDiv.append(hostLink);
                $("#infected_hosts").append(hostDiv);

                payloads.forEach((payload) => {
                    const userPayloadsDiv = $("<div class=\"user_payloads\"></div>");
                    const userPayloadsLink = $("Name: <a href=\"#\" class=\"payload_name_link\"" + payload['name'] + "</a>");
                    userPayloadsDiv.append(userPayloadsLink);
                    getPayload(host, payload['payload_id'], (data) => {
                        const payloadDataDiv = $("<div class=\"payload\">" + data + "</div>")
                        hostDiv.append(userPayloadsDiv);
                        hostDiv.append(payloadDataDiv);
                    });
                });
            });
        });

    });

    $("#search_form").submit(function (e) {
        return false;
    });
});
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

    var toggledMainState = 0;

    function toggleVisibility(someElement, shouldUseMainState) {
        if (shouldUseMainState === 1) {
            if(toggledMainState === 0) {
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
        } else {
            someElement.css('display', 'none');
        }
    }

    function toggleChildrenVisibility() {
        const children = $(this).children();
        children.each(function () {
            toggleVisibility($(this), 1);
        });
    }

    getInfectedHosts((hosts) => {
        hosts.forEach((host) => {
            getPayloads(host, (payloads) => {
                const hostDiv = $("<div class=\"host_name\"> </div>");
                const hostLink = $("<a href=\"#\" class=\"host_link\">" + host + "</a>");
                hostLink.click(function () {
                    $(this).siblings().each(toggleChildrenVisibility);
                    return false;
                });
                hostDiv.append(hostLink);
                $("#infected_hosts").append(hostDiv);

                payloads.forEach((payload) => {
                    const userPayloadsDiv = $("<div class=\"user_payloads\"></div>");
                    const userPayloadsLink = $("<div> Name: <a href=\"#\" class=\"payload_name_link\">" + payload['name'] + "</a> </div>");
                    userPayloadsLink.click(function () {
                        console.log($(this).closest('.user_payloads').siblings().each(function () {
                            toggleVisibility($(this));
                        }));
                        return false;
                    });
                    userPayloadsDiv.append(userPayloadsLink);
                    getPayload(host, payload['payload_id'], (data) => {
                        const payloadDataDiv = $("<div class=\"payload\">" + data + "</div>")
                        const containerDiv = $("<div></div>")
                        containerDiv.append(userPayloadsDiv);
                        containerDiv.append(payloadDataDiv);
                        hostDiv.append(containerDiv);
                    });
                });
            });
        });

    });

    $("#search_form").submit(function (e) {
        return false;
    });
});
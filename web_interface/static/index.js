console.log("hello world");

$(function(){
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

    $("#search_form").submit(function(e){
        getInfectedHosts((hosts) => {
            for(let host in hosts) {
                $("#infected_hosts").append("<li>" + host + "</li>")
            }
            // getPayloads(hosts[0], (payloads) => {
            //     getPayload(hosts[0], payloads[0]['payload_id'], (data) => {
            //         console.log(data);
            //     });
            // });
        });
        return false;
    });
});
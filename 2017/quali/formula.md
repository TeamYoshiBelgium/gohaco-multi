

$$SUM[r=1..requests](
    quantity(r) * (
        latency(endpoint(r)) - minEndpointVideoLatency(endpoint(r), video(r))
    )
) / SUM[r=1..requests](quantity(r))$$

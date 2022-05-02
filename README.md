# NTHU_alb_reserve

## Getting Start
Download the exe file [here](https://github.com/iwtba4188/reservation_of_nthualb/releases/tag/v2.0).

In the setting file, you need to fill the information as below.
```json
{
    "id": "110XXXXXX",
    "password": "yourpassword",
    "field1": "3",
    "time1": "12",
    "field2": "3",
    "time2": "13"
}
```

### Notice
- The "field" means the number you need.
- The "time" means the period you need. Be careful, it should be an integer between `""`. For exxample, `7:00~8:00` is `"1"`, `8:00~9:00` is `"2"`, and so on.


## Thanks
- Chrome extension [NTHU OAuth Decaptcha](https://github.com/justin0u0/NTHU-OAuth-Decaptcha) by [Justin0u0](https://github.com/justin0u0).

# haloinfinite
Library written in Python that wraps Halo Infinite API.

## Before start
It's unofficial, reverse-engineered, neither stable nor production ready Halo Infinite web API.

You need to [register an Azure Active Directory application](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app) and set a Client Secret for your application.

## Credits
Credits to [Den Delimarsky](https://github.com/dend) for the reverse-engineering. If you want to learn more then check his [Halo Infinite Web API blog series](https://den.dev/series/halo-infinite-web-api). Also you can use his [API wrapper written in C#](https://github.com/dend/grunt).

## Installing
```
pip install haloinfinite
```

## Usage
### Client instantiation
```
from haloinfinite.client import HaloInfiniteAPIClient as Client
client = Client(client_id, client_secret, user_token=None, xbox_user_token=None, xsts_xbox_token=None, xsts_halo_token=None, spartan_token=None, clearance_token=None)
```

### OAuth 2.0
#### Get authorization url
```
url = client.get_authorization_url(redirect_uri, scope=["Xboxlive.signin", "Xboxlive.offline_access"], state=None)
```

#### Exchange the code for an user token
```
user_token = client.exchange_code(redirect_uri, code)

# print(user_token.data)
{
    "token_type": "bearer",
    "expires_in": 3600,
    "scope": "XboxLive.signin XboxLive.offline_access",
    "access_token": "...",
    "refresh_token": "...",
    "user_id": "...",
}
```

#### Refresh user token
```
user_token = client.refresh_token(redirect_uri, user_token["refresh_token"])

# print(user_token.data)
{
    "token_type": "bearer",
    "expires_in": 3600,
    "scope": "XboxLive.signin XboxLive.offline_access",
    "access_token": "...",
    "refresh_token": "...",
    "user_id": "...",
}
```

#### Set user token
```
client.set_user_token(user_token)
```

#### Get xbox user token
```
xbox_user_token = client.get_xbox_user_token()

# print(xbox_user_token.data)
{
    "IssueInstant": "2022-02-06T01:00:03.6132203Z",
    "NotAfter": "2022-02-20T01:00:03.6132203Z",
    "Token": "...",
    "DisplayClaims": {"xui": [{"uhs": "..."}]},
}
```

#### Set xbox user token
```
client.set_xbox_user_token(token=xbox_user_token)
```

#### Get xsts xbox token
```
xsts_xbox_token = client.get_xsts_xbox_token()

# print(xsts_xbox_token.data)
{
    "IssueInstant": "2022-02-06T01:35:40.7628209Z",
    "NotAfter": "2022-02-06T17:35:40.7628209Z",
    "Token": "...",
    "DisplayClaims": {
        "xui": [
            {
                "gtg": "...",
                "xid": "...",
                "uhs": "...",
                "agg": "Adult",
                "usr": "...",
                "utr": "...",
                "prv": "...",
            }
        ]
    },
}
```

#### Set xsts xbox token
```
client.set_xsts_xbox_token(token=xsts_xbox_token)
```

#### Get xsts halo token
```
xsts_halo_token = client.get_xsts_xbox_token()

# print(xsts_halo_token.data)
{
    "IssueInstant": "2022-02-06T01:12:27.9108457Z",
    "NotAfter": "2022-02-06T05:12:27.9108457Z",
    "Token": "...",
    "DisplayClaims": {"xui": [{"uhs": "..."}]},
}
```

#### Set xsts halo token
```
client.set_xsts_halo_token(token=xsts_halo_token)
```

#### Get spartan token
```
spartan_token = client.get_xsts_xbox_token()

# print(spartan_token.data)
{
    "SpartanToken": "...",
    "ExpiresUtc": {"ISO8601Date": "2022-02-06T05:12:27Z"},
    "TokenDuration": "PT3H34M12.4226916S",
}
```

#### Set spartan token
```
client.set_spartan_token(token=spartan_token)
```

#### Get clearance token
```
clearance_token = client.get_clearance_token()

# print(clearance_token.data)
{
    "FlightConfigurationId": "...",
}
```

#### Set clearance token
```
client.set_clearance_token(token=clearance_id)
```

## Match API

#### Match privacy
```
response = client.match.get_match_privacy()

# print(response.data)
{'MatchmadeGames': 1, 'OtherGames': 2}
```

#### Match count
```
response = client.match.get_match_count()

# print(response.data)
{'CustomMatchesPlayedCount': 6, 'MatchesPlayedCount': 885, 'MatchmadeMatchesPlayedCount': 879, 'LocalMatchesPlayedCount': 0}
```

#### Match history
```
response = client.match.get_match_history()

# print(response.data)
{'Count': 25,
 'Links': {},
 'ResultCount': 25,
 'Results': [{'LastTeamId': 0,
              'MatchId': '...',
              'MatchInfo': {'ClearanceId': '...',
                            'Duration': 'PT9M22.8961519S',
                            'EndTime': '2022-02-05T23:30:32.564Z',
                            'GameVariantCategory': 9,
                            'LevelId': '...',
                            'LifecycleMode': 3,
                            'MapVariant': {'AssetId': '...',
                                           'AssetKind': 2,
                                           'VersionId': '...'},
                            'PlayableDuration': 'PT9M22.875S',
                            'Playlist': {'AssetId': '...',
                                         'AssetKind': 3,
                                         'VersionId': '...'},
                            'PlaylistExperience': 5,
                            'PlaylistMapModePair': {'AssetId': '...',
                                                    'AssetKind': 7,
                                                    'VersionId': '...'},
                            'SeasonId': 'Seasons/Season6.json',
                            'StartTime': '2022-02-05T23:20:39.923Z',
                            'TeamScoringEnabled': True,
                            'TeamsEnabled': True,
                            'UgcGameVariant': {'AssetId': '...',
                                               'AssetKind': 6,
                                               'VersionId': '...'}},
              'Outcome': 3,
              'PresentAtEndOfMatch': True,
              'Rank': 6},
              ...
 'Start': 0}
```

#### Match stats
```
response = client.match.get_match_stats(match_id)

# print(response.data)
{'MatchId': '...',
 'MatchInfo': {'ClearanceId': '...',
               'Duration': 'PT9M22.8961519S',
               'EndTime': '2022-02-05T23:30:32.564Z',
               'GameVariantCategory': 9,
               'LevelId': '...',
               'LifecycleMode': 3,
               'MapVariant': {'AssetId': '...',
                              'AssetKind': 2,
                              'VersionId': '...'},
               'PlayableDuration': 'PT9M22.875S',
               'Playlist': {'AssetId': '...',
                            'AssetKind': 3,
                            'VersionId': '...'},
               'PlaylistExperience': 5,
               'PlaylistMapModePair': {'AssetId': '...',
                                       'AssetKind': 7,
                                       'VersionId': '...'},
               'SeasonId': 'Seasons/Season6.json',
               'StartTime': '2022-02-05T23:20:39.923Z',
               'TeamScoringEnabled': True,
               'TeamsEnabled': True,
               'UgcGameVariant': {'AssetId': '...',
                                  'AssetKind': 6,
                                  'VersionId': '...'}},
 'Players': [...],
 'Teams': [...],
```

#### Match skill
```
response = client.match.get_match_skill(match_id, player_id)

# print(response.data)
{'Value': [{'Id': 'xuid(...)',
            'Result': {'Counterfactuals': {'SelfCounterfactuals': {'Deaths': 12.38441050555862,
                                                                   'Kills': 11.805217023995946},
                                           'TierCounterfactuals': {}},
                       'RankRecap': {'PostMatchCsr': {'InitialMeasurementMatches': 0,
                                                      'MeasurementMatchesRemaining': 0,
                                                      'NextSubTier': 0,
                                                      'NextTier': '',
                                                      'NextTierStart': 0,
                                                      'SubTier': 0,
                                                      'Tier': '',
                                                      'TierStart': 0,
                                                      'Value': 0},
                                     'PreMatchCsr': {'InitialMeasurementMatches': 0,
                                                     'MeasurementMatchesRemaining': 0,
                                                     'NextSubTier': 0,
                                                     'NextTier': '',
                                                     'NextTierStart': 0,
                                                     'SubTier': 0,
                                                     'Tier': '',
                                                     'TierStart': 0,
                                                     'Value': 0}},
                       'RankedRewards': None,
                       'StatPerformances': {'Deaths': {'Count': 9,
                                                       'Expected': 12.38441050555862,
                                                       'StdDev': 4.498181792537211},
                                            'Kills': {'Count': 13,
                                                      'Expected': 11.805217023995946,
                                                      'StdDev': 4.750282423640629}},
                       'TeamId': 0,
                       'TeamMmr': 1149.370133486992,
                       'TeamMmrs': {'0': 1149.370133486992,
                                    '1': 1151.942592441846}},
            'ResultCode': 0}]}
```

#### Match progression
```
response = client.match.get_match_progression(match_id)

# print(response.data)
{'ChallengeProgressState': [{'Id': '...',
                             'Path': 'ChallengeContent/ClientChallengeDefinitions/S1CapstoneChallenges/CSamuraiMedalKilljoy.json',
                             'PreviousProgress': 1,
                             'Progress': 3},
                            {'Id': '...',
                             'Path': 'ChallengeContent/ClientChallengeDefinitions/DailyChallenges/PlayNew/d0NPlayB1.json',
                             'PreviousProgress': 0,
                             'Progress': 1}],
 'ClearanceId': '...',
 'RewardId': '...'}
```

## Requirements
- requests
- python-dateutil

## Tests
- Not yet

## Contributing
We are always grateful for any kind of contribution including but not limited to bug reports, code enhancements, bug fixes, and even functionality suggestions.

#### You can report any bug you find or suggest new functionality with a new [issue](https://github.com/ingmferrer/haloinfinite/issues).

#### If you want to add yourself some functionality to the wrapper:
1. Fork it ( https://github.com/ingmferrer/haloinfinite )
2. Create your feature branch (git checkout -b my-new-feature)
3. Commit your changes (git commit -am 'Adds my new feature')
4. Push to the branch (git push origin my-new-feature)
5. Create a new Pull Request

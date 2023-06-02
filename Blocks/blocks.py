trend_blockss= [
		{
			"type": "divider"
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Test block with multi static select"
			},
			"accessory": {
				"type": "multi_static_select",
				"placeholder": {
					"type": "plain_text",
					"text": "Select options",
					"emoji": True
				},
				"options": [
					{
						"text": {
							"type": "plain_text",
							"text": "o2",
							"emoji": True
						},
						"value": "o2"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "telekom",
							"emoji": True
						},
						"value": "telekom"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "vodafone",
							"emoji": True
						},
						"value": "vodafone"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "congstar",
							"emoji": True
						},
						"value": "congstar"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "1und1",
							"emoji": True
						},
						"value": "1und1"
					}
				],
				"action_id": "trend-select"
			}
		}
	]

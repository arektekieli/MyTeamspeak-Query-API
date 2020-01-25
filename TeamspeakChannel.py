from TeamspeakAbstract import TeamspeakAbstract

class TeamspeakChannel(TeamspeakAbstract):
    def __init__(self, teamspeak, resultItem):
        self.teamspeak = teamspeak
        self.attributes = ['cid', 'channel_banner_gfx_url', 'channel_banner_mode', 'channel_codec', 'channel_codec_is_unencrypted', 'channel_codec_latency_factor', 'channel_codec_quality', 'channel_delete_delay', 'channel_description', 'channel_filepath', 'channel_flag_default', 'channel_flag_maxclients_unlimited', 'channel_flag_maxfamilyclients_inherited', 'channel_flag_maxfamilyclients_unlimited', 'channel_flag_password', 'channel_flag_permanent', 'channel_flag_semi_permanent', 'channel_forced_silence', 'channel_icon_id', 'channel_maxclients', 'channel_maxfamilyclients', 'channel_name', 'channel_name_phonetic', 'channel_needed_talk_power', 'channel_order', 'channel_password', 'channel_security_salt', 'channel_topic', 'channel_unique_identifier']
        
        for attr in self.attributes:
            setattr(self, attr, None)
        
        self.updateAttributes(resultItem)

    def update(self):
        x = self.teamspeak.channelinfo(self)
        self.updateAttributes(x)

    def toList(self):
        return [{attr: getattr(self, attr)} for attr in self.attributes]

    def toDict(self):
        res = {}
        for attr in self.attributes:
            res.update({attr: getattr(self, attr)})
            
        return res
    
        
from fastmcp.server.auth import TokenVerifier,AccessToken
class KeyVerifier(TokenVerifier):
    async  def verify_token(self,token:str)->AccessToken|None:
        print('verify_token',token)
        if token == "123456":
            return AccessToken(
                token=token,
                client_id="123456",
                scopes=['read']
            )
        else:
            return None

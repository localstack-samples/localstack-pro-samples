package cloud.localstack;

import com.auth0.jwk.Jwk;
import com.auth0.jwk.JwkProvider;
import com.auth0.jwk.JwkProviderBuilder;
import com.auth0.jwt.interfaces.RSAKeyProvider;

import java.net.MalformedURLException;
import java.net.URL;
import java.security.interfaces.RSAPrivateKey;
import java.security.interfaces.RSAPublicKey;

public class AwsCognitoRSAKeyProvider implements RSAKeyProvider {

    private final URL aws_kid_store_url;

    public AwsCognitoRSAKeyProvider(String aws_cognito_region, String aws_user_pools_id) {
        String url = String.format("https://cognito-idp.%s.amazonaws.com/%s/.well-known/jwks.json", aws_cognito_region, aws_user_pools_id);
        try {
            this.aws_kid_store_url = new URL(url);
        } catch (MalformedURLException e) {
            throw new RuntimeException(String.format("Invalid URL provided, URL=%s", url));
        }
    }


    @Override
    public RSAPublicKey getPublicKeyById(String kid) {
        try {
            JwkProvider provider = new JwkProviderBuilder(aws_kid_store_url).build();
            Jwk jwk = provider.get(kid);
            return (RSAPublicKey) jwk.getPublicKey();
        } catch (Exception e) {
            throw new RuntimeException(String.format("Failed to get JWT kid=%s from aws_kid_store_url=%s", kid, aws_kid_store_url));
        }
    }

    @Override
    public RSAPrivateKey getPrivateKey() {
        return null;
    }

    @Override
    public String getPrivateKeyId() {
        return null;
    }
}
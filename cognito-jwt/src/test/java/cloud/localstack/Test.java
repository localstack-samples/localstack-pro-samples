package cloud.localstack;

import java.net.MalformedURLException;
import java.net.URL;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

import com.auth0.jwt.JWT;
import com.auth0.jwt.Algorithm;
import com.auth0.jwt.Claim;
import com.auth0.jwk.JwkProvider;
import com.auth0.jwk.JwkProviderBuilder;
import com.auth0.jwt.interfaces.RSAKeyProvider;

public class Test {

    public static String TOKEN_USE = "use";
    public static String ACCESS = "access";
    public static String CLIENT_ID = "client_id";
    public static String USER_NAME = "user_name";
    public static String SCOPE = "scope";
    public static String ACCEPT_LEEWAY_SECONDS = 60;

    public void convert(@NonNull final String token) throws MalformedURLException {

        final URL kidStore = new URL(awsProperties.getCognito().getKidStoreUrl());
        final JwkProvider jwkProvider = new JwkProviderBuilder(kidStore).build();

        final DecodedJWT decodedJWT = JWT.decode(token);
        final AwsCognitoRSAKeyProvider awsCognitoRSAKeyProvider = new AwsCognitoRSAKeyProvider(jwkProvider);

        JWT.require(Algorithm.RSA256(awsCognitoRSAKeyProvider))
                .acceptLeeway(ACCEPT_LEEWAY_SECONDS)
                .withClaim(TOKEN_USE, ACCESS)
                .build()
                .verify(decodedJWT);

        final Claim clientIdClaim = decodedJWT.getClaim(CLIENT_ID);
        final Claim userNameClaim = decodedJWT.getClaim(USER_NAME);
        final Claim scopeClaim = decodedJWT.getClaim(SCOPE);

        final List<String> roles = Arrays.stream(scopeClaim.asString().split(" "))
                .map(scope -> scope.substring(scope.lastIndexOf("/") + 1))
                .collect(Collectors.toList());

        System.out.println("" + clientIdClaim + " " + userNameClaim + " " + roles);
        // return new InsureSignToken()
        //         .setClientId(clientIdClaim.asString())
        //         .setUserName(userNameClaim.asString())
        //         .setRoles(roles);
    }
}

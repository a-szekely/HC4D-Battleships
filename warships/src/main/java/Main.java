import io.improbable.keanu.tensor.dbl.DoubleTensor;
import io.improbable.keanu.vertices.bool.BooleanVertex;
import io.improbable.keanu.vertices.bool.probabilistic.BernoulliVertex;
import io.improbable.keanu.vertices.dbl.DoubleVertex;
import io.improbable.keanu.vertices.dbl.nonprobabilistic.ConstantDoubleVertex;
import io.improbable.keanu.vertices.dbl.probabilistic.GaussianVertex;
import io.improbable.keanu.vertices.dbl.probabilistic.UniformVertex;
import org.apache.commons.math3.analysis.function.Gaussian;
import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.HttpClientBuilder;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.message.BasicNameValuePair;
import org.json.JSONObject;
import org.omg.CORBA.NameValuePair;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.charset.Charset;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Vector;

public class Main {
    public static DoubleVertex updatePosterior(DoubleVertex previousPosterior, double[] position, boolean hit) {
        double sigma_bomb = 0.2; //how precise is the shooting
        DoubleVertex mu = new ConstantDoubleVertex(new double[]{position[0], position[1]}); //Oserved x and y coords of a hit
        DoubleVertex muCentre = new ConstantDoubleVertex(new double[]{0.5, 0.5}); //Oserved x and y coords of a hit
        GaussianVertex observedGaussian = new GaussianVertex(new long[]{2}, mu, sigma_bomb);
        DoubleVertex posteriorWithHoleAfterHit = new GaussianVertex(muCentre, 1);
        if (hit){
            GaussianVertex HoleAfterHitGaussian = new GaussianVertex(new long[]{2}, mu, sigma_bomb/4);
            //DoubleVertex posterior1 = new GaussianVertex(previousPosterior.times(observedGaussian), 1.0);
            DoubleVertex posterior = previousPosterior.times(observedGaussian);
            posteriorWithHoleAfterHit = posterior.minus(HoleAfterHitGaussian); // so that we don't hit again in the place we've already hit
        }
        else if (!hit){
            posteriorWithHoleAfterHit = previousPosterior.minus(observedGaussian);
        }
        return posteriorWithHoleAfterHit;
    }

    public static DoubleTensor samplePosterior(DoubleVertex Posterior) {
        int count = 1;
        DoubleTensor posteriorSamples = DoubleTensor.create(0, new long[]{1, 2});
        while (count < 100) {
            posteriorSamples = Posterior.sample();
            if (posteriorSamples.getValue(0) <= 1.0 && posteriorSamples.getValue(1) <= 1.0 && posteriorSamples.getValue(0) >= 0.0 && posteriorSamples.getValue(1) >= 0.0){
                System.out.println(posteriorSamples);
                break;
            }
            count++;
        }
        return posteriorSamples;
    }


    public static double calculateDistance(double mx_pos, double my_pos, double mx_sample, double my_sample) {
        double x_distance_squared = Math.pow(mx_pos - mx_sample, 2);
        double y_distance_squared = Math.pow(my_pos - my_sample, 2);
        double distance = Math.sqrt(x_distance_squared + y_distance_squared);
        return distance;
    }

    public static String convertInputToString(InputStream inputStream) throws IOException {

        StringBuilder stringBuilder = new StringBuilder();
        String line = null;

        try (BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(inputStream))) {
            while ((line = bufferedReader.readLine()) != null) {
                stringBuilder.append(line);
            }
        }
        return stringBuilder.toString();
    }

    public static String POSTRequest(double x, double y) {
        HttpClient httpClient = HttpClientBuilder.create().build(); //Use this instead

        try {
            HttpPost request = new HttpPost("http://localhost:5002/shot/");
            String input = "{\"player\":\"ai\",\"x\":\"" + Double.toString(x) + "\",\"y\":\"" + Double.toString(y) + "\"}";
            StringEntity params = new StringEntity(input);
            request.setEntity(params);
            HttpResponse response = httpClient.execute(request);
            HttpEntity entity = response.getEntity();
            InputStream content = entity.getContent();
            String answer = convertInputToString(content);
            return answer;


        }catch (Exception ex) {

            //handle exception here

        } finally {
            //Deprecated
            //httpClient.getConnectionManager().shutdown();
        }
        return "-1";
    }



    public static void main(String[] args) {
        double bomb_radius = 0.1;

        List x_positions = new ArrayList();
        List y_positions = new ArrayList();
        System.out.println("Elo Mordo!");
        UniformVertex uniformVertex = new UniformVertex(new long[]{2}, 0, 1);
        DoubleVertex currentPosterior = uniformVertex;
        DoubleTensor samples = uniformVertex.sample();
        int no_points = 0;
        int iteration = 1;
        while (iteration <= 10){ //later change until the end of the game
            int count = 1;
            DoubleTensor samplesFromPosterior = DoubleTensor.create(0, new long[]{1, 2});
            while (count < 100) {
                samplesFromPosterior = samplePosterior(currentPosterior);
                int i = 0;
                boolean validSample = true;
                if (no_points > 0){
                    while (i < no_points) { // check if the hit is not aiming at the already hit place
                        double x_pos = (double) x_positions.get(i);
                        double y_pos = (double) y_positions.get(i);
                        double x_sample = samplesFromPosterior.getValue(0);
                        double y_sample = samplesFromPosterior.getValue(1);
                        double distance = calculateDistance(x_pos, y_pos, x_sample, y_sample);
                        if (distance <= bomb_radius) {
                            validSample = false;
                            break;
                        }
                        i++;
                    }
                }

                if (validSample){
                    break;
                }
                System.out.println(count);
                count++;
            }

            double[] bombPosition = new double[]{samplesFromPosterior.getValue(0), samplesFromPosterior.getValue(1)}; //dummy hit position
            x_positions.add(bombPosition[0]);
            y_positions.add(bombPosition[1]);
            no_points = x_positions.size();

            double xHitOnMap = bombPosition[0]*600;
            double yHitOnMap = bombPosition[1]*600;
            String stringIfHit = POSTRequest(xHitOnMap, yHitOnMap);
            boolean ifHit = true;

            if (stringIfHit.equals("\"0\"")){
                ifHit = false;
                System.out.println("false!!!!!");
            }
            else if (stringIfHit.equals("\"1\"")){
                ifHit = true;
                System.out.println("true!!!!!");
            }
            else {
                System.out.println("wrong input from server");
            }

            double[] positionsForUpdate = new double[]{samplesFromPosterior.getValue(0), samplesFromPosterior.getValue(1)};
            DoubleVertex newPosterior = updatePosterior(currentPosterior, positionsForUpdate, ifHit);
            currentPosterior = newPosterior;

            //System.out.println(samplesFromPosterior);
            System.out.println(stringIfHit);
            iteration++;
        }

    }
}
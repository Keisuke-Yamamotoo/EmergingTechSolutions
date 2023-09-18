
import io.swagger.v3.core.util.Yaml
import io.swagger.v3.oas.models.OpenAPI

def spec = new OpenAPI().info(
        new io.swagger.v3.oas.models.info.Info()
                .title("Swagger Petstore")
                .version("1.0.3")
)
spec.servers.add(new io.swagger.v3.oas.models.servers.Server().url("https://petstore.swagger.io/v3"))
spec.components.schemas.put("Pet", 123)

Yaml.pretty().writeValue(System.out, spec)

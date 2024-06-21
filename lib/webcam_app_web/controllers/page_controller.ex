defmodule WebcamAppWeb.PageController do
  use WebcamAppWeb, :controller

  def home(conn, _params) do
    # The home page is often custom made,
    # so skip the default app layout.
    render(conn, :home, layout: false)
  end

  def index(conn, _params) do
    render(conn, "index.html")
  end

  def capture(conn, %{"image" => image_data}) do
    IO.puts("Proccesing image data")
    {:ok, binary} = Base.decode64(image_data)
    File.write("priv/captured_image.png", binary)

    case process_image("priv/captured_image.png") do
      {:ok, result} ->
        result = String.trim(result)
        IO.inspect(result, label: "result")
        json(conn, %{message: "Image processed successfully", result: result})
      {:error, reason} ->
        json(conn, %{message: "Error processing image", reason: reason})
    end
  end

  defp process_image(image_path) do
    script_path = Path.join("priv/", "recognize.py")
    System.cmd("python3", [script_path, image_path])
    |> case do
      {result, 0} -> {:ok, result}
      {error, _} -> {:error, error}
    end
  end
end

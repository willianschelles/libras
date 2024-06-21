defmodule WebcamAppWeb.ErrorJSONTest do
  use WebcamAppWeb.ConnCase, async: true

  test "renders 404" do
    assert WebcamAppWeb.ErrorJSON.render("404.json", %{}) == %{errors: %{detail: "Not Found"}}
  end

  test "renders 500" do
    assert WebcamAppWeb.ErrorJSON.render("500.json", %{}) ==
             %{errors: %{detail: "Internal Server Error"}}
  end
end

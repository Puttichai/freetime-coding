#include <vector>
#include <cmath>
#include <iostream>
#include <SFML/Graphics.hpp>

size_t windowWidth = 400;
size_t windowHeight = 300;
const size_t numMaxHistory = 100;
const sf::Vector3f defaultColor(0, 255, 0);
struct MyPoint
{
    MyPoint(const float radius) : radius(radius), pos(0, 0), vel(0.6, 1), iCurrentIndex(0), _va(sf::LineStrip, numMaxHistory - 1)
    {
	vPosHistory.reserve(numMaxHistory);
	for( size_t i = 0; i < numMaxHistory; ++i ) {
	    vPosHistory.emplace_back(sf::Vector2f(0, 0));
	}
    }

    void Save()
    {
	vPosHistory[iCurrentIndex] = pos; // record the current position
	++iCurrentIndex;
	iCurrentIndex = iCurrentIndex % numMaxHistory;
    }

    /// \brief For drawing the trace of this point.
    const sf::VertexArray GetVertexArray()
    {
	// sf::VertexArray va(sf::LineStrip, numMaxHistory - 1);
	for( size_t vaIndex = 0; vaIndex < numMaxHistory - 1; ++vaIndex ) {
	    // Start populating va from the last (oldest) entry of vPosHistory so that more recent entries get drawn later.
	    size_t actualIndex = (iCurrentIndex + 1 + vaIndex)%numMaxHistory;
	    _va[vaIndex].position = vPosHistory[actualIndex];

	    const float ratio = (float(vaIndex)/float(numMaxHistory));
	    const sf::Vector3f currentColor = ratio * defaultColor;
	    _va[vaIndex].color = sf::Color(static_cast<sf::Uint8>(currentColor.x), static_cast<sf::Uint8>(currentColor.y), static_cast<sf::Uint8>(currentColor.z));
	}
	return _va;
    }
    
    sf::Vector2f pos, vel;
    float radius;
    std::vector<sf::Vector2f> vPosHistory;
    size_t iCurrentIndex;
    sf::VertexArray _va; // cache
};

void UpdatePointPosition(MyPoint& point)
{
    float step = 1;
    point.pos.x += point.vel.x*step;
    point.pos.y += point.vel.y*step;
    if( point.pos.x >= windowWidth || point.pos.x <= 0 ) {
	point.vel.x *= -1.0;
    }
    if( point.pos.y >= windowHeight || point.pos.y <= 0 ) {
	point.vel.y *= -1.0;
    }
}

int main(int argc, char* argv[])
{
    sf::ContextSettings settings;
    settings.antialiasingLevel = 8;

    sf::RenderWindow window(sf::VideoMode(windowWidth, windowHeight), "My Window", sf::Style::Default, settings);
    window.setVerticalSyncEnabled(true);
    
    const float radius = 5;
    MyPoint point(radius);

    sf::RenderTexture traces;
    traces.create(windowWidth, windowHeight);
    traces.clear(sf::Color::Black);
    traces.display();

    sf::RenderTexture blurTexture, renderer;
    blurTexture.create(windowWidth, windowHeight);
    renderer.create(windowWidth, windowHeight);
    
    while( window.isOpen() ) {
	sf::Event event;
        while (window.pollEvent(event))
        {
            // Close window : exit
            if( event.type == sf::Event::Closed ) {
                window.close();
	    }
        }
	UpdatePointPosition(point);
	point.Save();
	    
	window.clear(sf::Color::Black);
	
	window.draw(point.GetVertexArray());

	sf::CircleShape ballRepresentation(radius);
	ballRepresentation.setPointCount(64);
	ballRepresentation.setFillColor(sf::Color(static_cast<sf::Uint8>(0), static_cast<sf::Uint8>(255), static_cast<sf::Uint8>(0)));
	ballRepresentation.setOrigin(radius, radius);
	ballRepresentation.setPosition(point.pos);
	window.draw(ballRepresentation);
	
	window.display();
    }
    return EXIT_SUCCESS;
}

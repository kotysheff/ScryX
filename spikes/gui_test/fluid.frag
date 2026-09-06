#version 440

layout(location = 0) in vec2 qt_TexCoord0;
layout(location = 0) out vec4 fragColor;

layout(std140, binding = 0) uniform buf {
    mat4 qt_Matrix;
    float qt_Opacity;
    float iTime;
    vec2 iMouse;
};

void main() {
    vec2 uv = qt_TexCoord0;

    float waveX = sin(uv.y * 10.0 + iTime * 2.0) * 0.05;
    float waveY = cos(uv.x * 10.0 + iTime * 1.5) * 0.05;

    vec2 mouseDist = uv - iMouse;
    float mouseEffect = smoothstep(0.3, 0.0, length(mouseDist)) * 0.08;

    vec2 distortedUv = uv + vec2(waveX, waveY) + (mouseDist * mouseEffect);

    float r = sin(distortedUv.x * 5.0 + iTime) * 0.5 + 0.5;
    float g = cos(distortedUv.y * 5.0 - iTime) * 0.5 + 0.5;
    float b = sin((distortedUv.x + distortedUv.y) * 3.0 + iTime * 2.0) * 0.5 + 0.5;

    vec3 finalColor = vec3(r, g, b) * 0.25;

    float line = 1.0 - smoothstep(0.0, 0.02, abs(sin(distortedUv.x * 10.0 + iTime) - distortedUv.y * 2.0));
    finalColor += vec3(0.0, 0.8, 1.0) * line * 0.3;

    fragColor = vec4(finalColor, 1.0) * qt_Opacity;
}

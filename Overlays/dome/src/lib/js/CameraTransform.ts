export interface CameraTransform {
    position: Position;
    rotation: Rotation;
}

export interface Position {
    X: number;
    Y: number;
    Z: number;
}

export interface Rotation {
    X: number;
    Y: number;
    Z: number;
    W: number;
}
